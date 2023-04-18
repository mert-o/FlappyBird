import mediapipe as mp
import cv2
from threading import Thread
import math
import numpy as np
import time
class media:
   
        
    def __init__(self, vc):
            self.videocapture = vc

            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_drawing_styles = mp.solutions.drawing_styles
            self.mp_face_mesh = mp.solutions.face_mesh
            self.drawing_spec = self.mp_drawing.DrawingSpec(
                thickness=1, circle_radius=1)
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)
            
            self.smile_level = -1
            self.stop = False
            self.frame = None
            self.verbose = False
            self.star_img = cv2.imread('assets/sprites/star.png',cv2.IMREAD_UNCHANGED)
            self.org_img = None
            
            self.max_lip_height = 1
            self.max_mcd = -1
            self.max_mw = -1
            self.max_ed = -1
            self.smile_buffer = []
            self.buffer_size = 3

            self.num_stars = 0
            self.fd = None
            self.configured = False
            self._lastFaceDetected = -1

            # lip distance, mouth center y and corner y difference, mouth width, eye height
            self.weights = [0.35, 0.0, 0.5, 0.15]

    def start(self):
            Thread(target=self.gen, args=()).start()
            return self

    
    def gen(self):

        while not self.stop:
            if self.videocapture.frame is not None:
                image = self.videocapture.frame.copy()
                if self.org_img is None:
                     self.org_img = image.copy()
            else: continue
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            if not (image == self.org_img).all():
                
                image.flags.writeable = False
                img2 = image.copy()
                
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                results = self.face_mesh.process(image)
                height, width, _ = image.shape
                
                
                if results.multi_face_landmarks:
                    self._lastFaceDetected = -1
                    
                    for face_landmarks in results.multi_face_landmarks:
                        
                        self.mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self.mp_drawing_styles
                        .get_default_face_mesh_tesselation_style())
                        
                        self.mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self.mp_drawing_styles
                        .get_default_face_mesh_contours_style())
                        
                        self.mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=self.mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self.mp_drawing_styles
                        .get_default_face_mesh_iris_connections_style())
                        
                    #cv2.circle(image,(int(face_landmarks.landmark[14].x*image.shape[1]),int(face_landmarks.landmark[14].y*image.shape[0])),1,(255,0,0),-1)
                    #cv2.circle(image,(int(face_landmarks.landmark[17].x*image.shape[1]),int(face_landmarks.landmark[17].y*image.shape[0])),1,(0,0,255),-1)
                    #cv2.circle(image,(int(face_landmarks.landmark[0].x*image.shape[1]),int(face_landmarks.landmark[0].y*image.shape[0])),1,(255,0,0),-1)
                    #cv2.circle(image,(int(face_landmarks.landmark[13].x*image.shape[1]),int(face_landmarks.landmark[13].y*image.shape[0])),1,(0,0,255),-1)
                    
                        
                    face_landmarks = results.multi_face_landmarks[0]
                    
                    # Compute the distance between the top and bottom lips
                    upper_lip_landmark_ids = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
                    lower_lip_landmark_ids = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
                    upper_lip_points = [face_landmarks.landmark[idx] for idx in upper_lip_landmark_ids]
                    lower_lip_points = [face_landmarks.landmark[idx] for idx in lower_lip_landmark_ids]
                    upper_lip_distance = sum(abs(upper_lip_points[i].y - lower_lip_points[i].y) for i in range(len(upper_lip_points))) / len(upper_lip_points)
                    
                    # Compute the angle between the mouth corners and the center of the lips
                    mouth_corner_landmark_ids = [61, 291]
                    mouth_center_landmark_id = 13
                    mouth_corner_points = [face_landmarks.landmark[idx] for idx in mouth_corner_landmark_ids]
                    mouth_center_point = face_landmarks.landmark[mouth_center_landmark_id]
                    mouth_corner_angle =(math.atan2(mouth_corner_points[0].y - mouth_center_point.y, mouth_corner_points[0].x - mouth_center_point.x))
                    
                    #mouth center corner y difference
                    m_c_difference = (mouth_center_point.y - mouth_corner_points[0].y ) + (mouth_center_point.y - mouth_corner_points[1].y ) 
                    
                    #mouth width
                    mouth_width = np.linalg.norm((mouth_corner_points[0].x-mouth_corner_points[1].x,mouth_corner_points[0].y-mouth_corner_points[1].y))

                    #eye distance
                    t_eye_points = [386,159]#[362,398,384,385,386,387,388,466,263,33,246,161,160,159,158,157,173,133]
                    b_eye_points = [374,145]#[362,382,381,380,374,373,390,249,263,33,7,163,144,145,153,154,155,133]

                    upper_eye_points = [face_landmarks.landmark[idx] for idx in t_eye_points]
                    bottom_eye_points = [face_landmarks.landmark[idx] for idx in b_eye_points]
                    eye_distance = sum(abs(upper_eye_points[i].y - bottom_eye_points[i].y) for i in range(len(upper_eye_points))) / len(upper_lip_points)
                    #eye_distance = 1/eye_distance

                    nuld = upper_lip_distance / self.max_lip_height
                    nmcd = m_c_difference / self.max_mcd 
                    if nmcd <0: nmcd = 0
                    nmw = mouth_width / self.max_mw
                    ned = (self.max_ed-eye_distance) / self.max_ed
                    
                    smile_score = self.weighted_smile_score(nuld, nmcd,nmw,ned, self.weights)
                    num_bins = 30
                    bin_width = 1 / num_bins
                    smile_degree = int(smile_score // bin_width)
                    #self.smile_level = smile_degree
                    #print(smile_degree,nuld,nmcd,nmw,ned)
                    if upper_lip_distance > self.max_lip_height: self.max_lip_height = upper_lip_distance
                    if m_c_difference > self.max_mcd : self.max_mcd = m_c_difference
                    if mouth_width > self.max_mw: self.max_mw = mouth_width
                    if eye_distance > self.max_ed: self.max_ed = eye_distance
                    
                    self.smile_buffer.append(smile_score)
                    if len(self.smile_buffer) > self.buffer_size:
                        self.smile_buffer.pop(0)
                    if len(self.smile_buffer) == self.buffer_size:
                        
                        mean_score = sum(self.smile_buffer) / len(self.smile_buffer)
                        threshold = 0.3  # Adjust this value based on your use case
                        filtered_scores = [score for score in self.smile_buffer if abs(score - mean_score) <= threshold * mean_score]

                        # Calculate the mean of the remaining scores
                        if len(filtered_scores) > 0:
                            self.smile_level= max(filtered_scores)
                        else:
                            # If all scores are considered anomalies, use the original mean
                            self.smile_level = mean_score
                        
                        num_bins = 30
                        bin_width = 1 / num_bins
                        self.smile_level = int(self.smile_level // bin_width)

                    """ lip_distance_weight = 0.2
                    mouth_corner_diff_weight = 0.2
                    mouth_width_weight = 0.3
                    eye_distance_weight = 0.3

                    # Calculate the weighted smile score
                    smile_score = (
                        lip_distance_weight * nuld +
                        mouth_corner_diff_weight * nmcd +
                        mouth_width_weight * nmw +
                        eye_distance_weight * ned
                    )

                    # Add the smile score to the buffer
                    self.smile_buffer.append(smile_score)

                    # Keep the buffer size fixed
                    if len(self.smile_buffer) > self.buffer_size:
                        self.smile_buffer.pop(0)

                    # Calculate the smile level using a rolling window
                    if len(self.smile_buffer) == self.buffer_size:
                        # Calculate the rolling mean of the smile scores
                        window_size = 5
                        rolling_mean_scores = np.convolve(self.smile_buffer, np.ones(window_size)/window_size, mode='valid')
                        
                        # Calculate the interquartile range (IQR) and use it to filter outliers
                        Q1, Q3 = np.percentile(rolling_mean_scores, [25, 75])
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR

                        filtered_scores = [score for score in rolling_mean_scores if lower_bound <= score <= upper_bound]

                        # Calculate the mean of the remaining scores
                        if len(filtered_scores) > 0:
                            self.smile_level = max(filtered_scores)
                        else:
                            # If all scores are considered anomalies, use the original mean
                            self.smile_level = np.mean(rolling_mean_scores)

                        self.smile_level *= -1
                        # Convert the smile level to a discrete value
                        num_bins = 30
                        bin_width = 1 / num_bins
                        self.smile_level = int(self.smile_level // bin_width) """

                    image.flags.writeable = False
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    image = cv2.putText(image, str(self.smile_level), (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    forehead_point = face_landmarks.landmark[10]
                    nose_tip_point = face_landmarks.landmark[4]

                    # Calculate the center of the head
                    head_center_x = int(forehead_point.x * width)
                    head_center_y = int(forehead_point.y * height)
                    # Resize the star image if necessary
                    star_height, star_width = self.star_img.shape[:2]
                    scale_factor_big = 0.3
                    scale_factor = 0.2  # Adjust this value based on your use case
                    middle_star = cv2.resize(self.star_img, (int(star_width * scale_factor_big), int(star_height * scale_factor_big)), interpolation=cv2.INTER_AREA)
                    side_star = cv2.resize(self.star_img, (int(star_width * scale_factor), int(star_height * scale_factor)), interpolation=cv2.INTER_AREA)
                    middle_star_x = head_center_x - middle_star.shape[1] // 2
                    middle_star_y = head_center_y - middle_star.shape[0] * 2


                    left_star_x = middle_star_x - side_star.shape[1] // 2
                    left_star_y = middle_star_y + (middle_star.shape[0] - side_star.shape[0]) // 2

                    right_star_x = middle_star_x + middle_star.shape[1] - side_star.shape[1] // 2
                    right_star_y = left_star_y
                    
                    #star rotation
                    left_eye_point = face_landmarks.landmark[33]
                    right_eye_point = face_landmarks.landmark[263]

                    # Calculate the angle between the eyes
                    rotation_angle = math.degrees(math.atan2(right_eye_point.y - left_eye_point.y, right_eye_point.x - left_eye_point.x))

                    if self.num_stars == 1:
                        for i in range(middle_star.shape[0]):
                            for j in range(middle_star.shape[1]):
                                if middle_star[i,j,3] != 0:
                                    x = middle_star_x + j
                                    y = middle_star_y + i 
                                    if 0<= x < width and 0<=y<height:
                                        img2[y,x] = middle_star[i,j,:3]

                    elif self.num_stars % 2 == 0 and self.num_stars != 0:
                        middle1_x = head_center_x - middle_star.shape[1] + 2
                        middle2_x = head_center_x - 2
                        middle_y = head_center_y - middle_star.shape[0] * 2
                        ns = int((self.num_stars - 2) / 2)
                        side_y = int(middle_y + middle_star.shape[0] * 0.2)
                        
                        for star in range(ns):
                            for i in range(side_star.shape[0]):
                                for j in range(side_star.shape[1]):
                                    if side_star[i, j, 3] != 0:
                                        margin = side_star.shape[1] * (ns - star) / 2
                                        x = int(head_center_x - middle_star.shape[1] - margin) + j
                                        y = side_y + i
                                        if 0 <= x < width and 0 <= y < height:
                                            img2[y, x] = side_star[i, j, :3]
                                        x = int(head_center_x + middle_star.shape[1] + margin) - j
                                        y = side_y + i
                                        if 0 <= x < width and 0 <= y < height:
                                            img2[y, x] = side_star[i, j, :3]

                        for i in range(middle_star.shape[0]):
                            for j in range(middle_star.shape[1]):
                                if middle_star[i, j, 3] != 0:
                                    x1 = middle1_x + j
                                    x2 = middle2_x + j
                                    y = middle_y + i
                                    if 0 <= x1 < width and 0 <= y < height:
                                        img2[y, x1] = middle_star[i, j, :3]
                                    if 0 <= x2 < width and 0 <= y < height:
                                        img2[y, x2] = middle_star[i, j, :3]

                    elif self.num_stars!= 0:  # Number of stars is odd
                        ns = (self.num_stars - 1) // 2
                        middle_x = head_center_x - middle_star.shape[1] // 2
                        middle_y = head_center_y - middle_star.shape[0] * 2
                        side_y = int(middle_y + middle_star.shape[0] * 0.2)

                        for star in range(ns):
                            for i in range(side_star.shape[0]):
                                for j in range(side_star.shape[1]):
                                    if side_star[i, j, 3] != 0:
                                        margin = side_star.shape[1] * (ns - star) / 2
                                        x = int(head_center_x - middle_star.shape[1] // 2 - margin) + j
                                        y = side_y + i
                                        if 0 <= x < width and 0 <= y < height:
                                            img2[y, x] = side_star[i, j, :3]
                                        x = int(head_center_x + middle_star.shape[1] // 2 + margin) - j
                                        y = side_y + i
                                        if 0 <= x < width and 0 <= y < height:
                                            img2[y, x] = side_star[i, j, :3]

                        for i in range(middle_star.shape[0]):
                            for j in range(middle_star.shape[1]):
                                if middle_star[i, j, 3] != 0:
                                    x = middle_x + j
                                    y = middle_y + i
                                    if 0 <= x < width and 0 <= y < height:
                                        img2[y, x] = middle_star[i, j, :3]

                                                        
                    self.frame = image
                    self.org_img = image
                    #img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
                    self.fd = img2
                else:
                    if self._lastFaceDetected == -1:
                        self._lastFaceDetected = time.time()
                    if time.time() - self._lastFaceDetected > 5 and self._lastFaceDetected != -1:
                        self.configured = False
                        self.smile_level = -1

    def stop_media(self):
        self.stop = True

    def weighted_smile_score(self,nuld, nmcd,nmw,ned, weights):
        weighted_score = (nuld * weights[0] +
                        nmcd * weights[1] +
                        nmw * weights[2]+
                        ned * weights[3])
        return weighted_score

    def rotate_image(image, angle):
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        scale = 1.0

        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height), borderMode=cv2.BORDER_TRANSPARENT)

        return rotated_image