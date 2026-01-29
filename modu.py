#!/usr/bin/env python
# coding: utf-8

# In[12]:


def modulation(hp_data):
    
    import numpy as np

    def threed_ang(A, B):
        A = np.asarray(A)
        B = np.asarray(B)

        # Calculate the norms and dot product
        norm_A = np.linalg.norm(A, axis=1)
        norm_B = np.linalg.norm(B, axis=1)
        dot_product = np.einsum('ij,ij->i', A, B)

        # Calculate the cross product
        cross_product = np.cross(A, B)

        # Calculate the norm of the cross product
        norm_cross_product = np.linalg.norm(cross_product, axis=1)

        # Calculate the angle
        theta = np.degrees(np.arctan2(norm_cross_product, dot_product))

        return theta


    def uj(beta, ang1, n1, a1):
        n2 = n1 * np.cos(np.radians(beta)) / (1 - (np.sin(np.radians(beta)) * np.cos(np.radians(ang1)))**2)

        term1 = a1 * np.cos(np.radians(beta)) / (1 - (np.sin(np.radians(beta)) * np.cos(np.radians(ang1)))**2)
        term2_a = (n1**2) * np.sin(2 * np.radians(ang1)) * (np.cos(np.radians(beta)) * (np.sin(np.radians(beta))**2))
        term2_b = (1 - (np.sin(np.radians(beta)) * np.cos(np.radians(ang1)))**2)**2
        term2 = term2_a / term2_b
        a2 = term1 - term2

        return n2, a2

    # Define points
    p1 = hp_data[:, 0:3]
    p2 = hp_data[:, 3:6]
    p3 = hp_data[:, 6:9]
    p4 = hp_data[:, 9:12]

    # Compound angles
    beta1 = (180- threed_ang(p1 - p2, p3 - p2)).reshape(-1,1)
    beta2 = (180- threed_ang(p4 - p3, p2 - p3)).reshape(-1,1)

    # Driver-UJ1 Conditions
    n1 = 1
    a1 = 1

    # Rotational Position / Angle of rotation of Driver & Driven of both UJ1 & Uj2
    ang1 = np.linspace(0, 180, 720)
    ang2_a = np.degrees(np.arctan2(np.sin(np.radians(ang1)), np.cos(np.radians(beta1)) * np.cos(np.radians(ang1))))
    ang2_b = ang2_a + 90
    ang3 = np.degrees(np.arctan2(np.sin(np.radians(ang2_b)), np.cos(np.radians(beta2)) * np.cos(np.radians(ang2_b))))

    # Angular velocities of Driver & Driven of Uj2 (IMS & Pinion)
    n2, a2 = uj(beta1, ang1, n1, a1)
    n3, a3 = uj(beta2, ang2_b, n2, a2)
    modulation = ((np.max(n3, axis = 1) - np.min(n3, axis = 1)) * 100).reshape(-1,1)
    return modulation




# In[ ]:




