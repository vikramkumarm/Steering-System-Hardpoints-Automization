  
def hp(rack_pos,A,AA_prime, col_ang_range , col_len_range, E, centre_distance, pinion_length_range, offset_angle_range,
               mount_angle_range, max_UJ1_ang, max_UJ2_ang, max_diff_in_UJ_angles, ss_col_angle, ss_col_length,  ss_pinion_length, ss_offset_angle, ss_mount_angle):
    import os
    import numpy as np
    from modu import modulation
    A                          = np.array(A)
    E                          = np.array(E)
    ED                         = centre_distance
    col_ang                    = np.transpose(np.arange(col_ang_range[0], col_ang_range[1], ss_col_angle))
    col_len                    = np.transpose(np.arange(col_len_range[0], col_len_range[1] +1, ss_col_length))
    CD_range                   = np.transpose(np.arange(pinion_length_range[0], pinion_length_range[1], ss_pinion_length))
    off_ang_range              = np.transpose(np.arange(offset_angle_range[0], offset_angle_range[1],ss_offset_angle ))
    mount_ang_range            = np.transpose(np.arange(mount_angle_range[0],mount_angle_range [1], ss_mount_angle))
    diff_UJ_threshold          = max_diff_in_UJ_angles
        
        
    temp = len(col_len)
    col_len = np.repeat(col_len, len(col_ang))
    col_ang = np.tile(col_ang, temp)
    col_len = col_len.reshape(-1,1)
    col_ang = col_ang.reshape(-1,1)
    
    
    # 
    # 
    # ---
    # ___Computing B Point___
    # 
    
    # In[14]:
    
    
    def B_point(A, col_len, col_ang):
        dx = col_len * np.cos(np.radians(col_ang))
        dz = col_len * np.sin(np.radians(col_ang))   
        B = A - (np.hstack((dx, np.zeros_like(dx), dz)))
        return B
    
    
    # ---
    # ___Computing D point from E___
    
    # In[15]:
    
    
    def D_point(E, ED, ang, rack_pos):
        if rack_pos == 'Rack ahead':
            dx = ED*np.cos(ang*np.pi/180)
            dz = ED*np.sin(ang*np.pi/180)
            D = [E[0] + dx, E[1], E[2] - dz]
            D = np.array(D)
        elif rack_pos == 'Rack behind':
            dx = ED*np.cos(ang*np.pi/180)
            dz = ED*np.sin(ang*np.pi/180)
            D = [E[0] - dx, E[1], E[2] + dz]
            D = np.array(D)            
        return D
    
    
    # ---
    # ___Computing C point by incorporating offset and mounting angle contraints___
    
    # In[16]:
    
    
    def C_point( D, pin_len, theta1, theta2 ):
        
        #theta1 - mounting ang
        #theta2 - offset ang
        
        the1 = theta1*np.pi/180
        the2 = theta2*np.pi/180
        l = pin_len   
        a = l*np.cos(the2)*np.cos(the1)
        b = l*np.cos(the2)*np.sin(the1)
        c = l*np.sin(the2)
        C_point = D + np.array([a, c, b])
        return C_point
    
    
    # --- 
    # ___function for evaluating angle between vectors___
    
    # In[17]:
    
    
    def comp_ang(vector1, vector2):
        dot_product = np.sum(vector1 * vector2, axis=-1)
        magnitude_vector1 = np.linalg.norm(vector1, axis=-1)
        magnitude_vector2 = np.linalg.norm(vector2, axis=-1)
        cosine_theta = dot_product / (magnitude_vector1 * magnitude_vector2)
        angle_radians = np.arccos(np.clip(cosine_theta, -1.0, 1.0))
        angle_degrees = np.degrees(angle_radians)
        return angle_degrees.reshape(-1,1)
    
    
    
    # In[18]:
    
    
    import numpy as np
    import math
    
    def twodang(A, B):
        theta = math.degrees(np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))))
        return theta
    
    
    # In[19]:
    
    
    def append_data(E, d_pt, c_pt, b_pt, A, col_len, col_ang, pin_len, uj1, uj2,mount_angle, offset_angle,data,selected_data):
        selected_data = selected_data.flatten()
        diff_uj = abs(uj1-uj2)[selected_data]
        uj1 = uj1[selected_data]
        uj2 = uj2[selected_data]
        b_pt = b_pt[selected_data]
        length = len(uj1)
        A = np.tile(A, (length,1))
        c_pt = np.tile(c_pt, (length,1))
        d_pt = np.tile(d_pt, (length,1))
        E = np.tile(E, (length,1))
        
        mount_angle = np.tile(mount_angle, (length,1))
        offset_angle = np.tile(offset_angle, (length,1))
        
        col_len = col_len[selected_data]
        col_ang = col_ang[selected_data]
        
        i_shaft_len = np.sqrt( (np.sum(  (np.square(b_pt - c_pt)),  axis = 1)).reshape(-1,1))
        pin_len = np.tile(pin_len, (length,1))
        
        data.append(np.concatenate((A, b_pt, c_pt, d_pt, E, col_len, col_ang, i_shaft_len, pin_len,  mount_angle, offset_angle, uj1, uj2, diff_uj), axis = 1))
        return data
        
        
    # def write_data_to_excel(p_data):

    #     current_directory = os.getcwd()
    #     file_name = 'Book1.xlsx'
    #     existing_file_path = os.path.join(current_directory, file_name)
    
    #     # Check if the file exists
    #     if os.path.isfile(existing_file_path):
    #         # File exists, open in append mode
    #         with pd.ExcelWriter(
    #             existing_file_path, 
    #             mode="a",
    #             engine="openpyxl",
    #             if_sheet_exists="replace",
    #         ) as writer:
    #             p_data.to_excel(writer, sheet_name="Sheet1")
    #     else:
    #         # File doesn't exist, create and write data
    #         with pd.ExcelWriter(
    #             existing_file_path, 
    #             mode="w",
    #             engine="openpyxl",
    #         ) as writer:
    #             p_data.to_excel(writer, sheet_name="Sheet1")
                
        ###### this is to write data into csv file#############

    def write_data_to_excel(p_data):
        import os
        file_name = "Book1.csv"
        current_directory = os.getcwd()
        existing_file_path = os.path.join(current_directory, file_name)
        
        # Check if the file exists
        if os.path.isfile(existing_file_path):
            # Append without writing headers again   
            p_data.to_csv(file_name, mode="a")
        else:
            # Create file and write data
            p_data.to_csv(file_name, mode="w")



    
    
    # ---
    # ---
    # __Script for Automated extraction of steering system co-ordinates incorporating the above constaints__
    
    # In[45]:
    
    
    data = []
    
    for pin_len in  CD_range:
        for offset_angle in off_ang_range:
            for mount_angle in mount_ang_range:
                gear_ang = 90 - mount_angle
                d_pt     = D_point(E, ED, gear_ang, rack_pos)
                c_pt     = C_point(d_pt,pin_len ,mount_angle,offset_angle)
                A_prime  = B_point(A, AA_prime, col_ang)
                b_pt     = B_point(A_prime, col_len, col_ang )
                uj1      = comp_ang((b_pt - c_pt),  (A - b_pt))
                uj2      = comp_ang(c_pt - d_pt, (b_pt - c_pt) )
                selected_data = ((abs(uj1-uj2) < diff_UJ_threshold)  &  (uj1 < max_UJ1_ang)  & (uj2 < max_UJ1_ang))
                append_data(E, d_pt, c_pt, b_pt, A, col_len, col_ang, pin_len, uj1, uj2,mount_angle, offset_angle,data,selected_data)
    
    

    
    import pandas as pd
    try:
        
        data = [arr for arr in data if arr.size > 0]
        
        if len(data) == 0:
            valid_ind = 0
            
        else:  
               
            data = np.vstack(data)
            modu_col = modulation(data[:, 0:12])
            if data.shape[1] == 24:
                data = np.insert(data, data.shape[1], modu_col.flatten(), axis = 1)
            else:
                pass
        
        
            sorted_indices = np.argsort( data[:,-1])
            data = data[sorted_indices]
            data[:,0:-2] = np.round(data[:,0:-2], 2)
            data[:,-2:] = np.round(data[:,-2:], 5)
        
            col_name1 = np.array(['A', 'A','A','B', 'B','B','C', 'C','C', 'D','D','D', 'E','E','E', 'Column length', 'Column angle',
                        'I-shaft length', 'Pinion length'  , 'Mounting angle', 'Offset angle', 'UJ1 angle', 'UJ2 angle', 'diff in UJ angles', 'Modulation (%)'])
        
        
        
            col_name2 = np.array(['x','y','z',   'x','y','z',  'x','y','z',   'x','y','z',   'x','y','z', ' ', ' ', ' ',
                        ' ', ' ', ' ', ' ', ' ', ' ', ' '])
        
            col_name = pd.MultiIndex.from_arrays([col_name1, col_name2], names =['Parameter' , ' '])
        
        
            p_data = pd.DataFrame(data, columns = col_name)                
            write_data_to_excel(p_data)
            valid_ind = p_data.shape[0]
        
              
    except:
        valid_ind = -1
        
    return valid_ind
    







