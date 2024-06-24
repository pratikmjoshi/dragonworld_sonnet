import math
from OpenGL.GL import *
from OpenGL.GLU import *

# def set_material(r, g, b, alpha=1.0):
#     ambient = [r * 0.7, g * 0.7, b * 0.7, alpha]
#     diffuse = [r * 1.2, g * 1.2, b * 1.2, alpha]
#     specular = [0.5, 0.5, 0.5, alpha]
#     glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
#     glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
#     glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
#     glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 32.0)

def set_material(r, g, b, alpha=1.0):
    glColor4f(r, g, b, alpha)

def create_sphere(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)

def create_cylinder(base, top, height, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluCylinder(quadric, base, top, height, slices, stacks)
    gluDeleteQuadric(quadric)

def create_wing(size, segments, r, g, b, alpha):
    set_material(r, g, b, alpha)
    # set_material(r,g,b,alpha)
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    for i in range(segments + 1):
        theta = i * math.pi / segments
        x = size * math.sin(theta)
        y = size * math.cos(theta)
        glNormal3f(0, 0, 1)
        glVertex3f(x, y, 0)
    glEnd()

def render_teeth():
    set_material(0.9, 0.9, 0.9)  # Off-white color for teeth
    for i in range(5):  # Render 5 teeth
        glPushMatrix()
        glTranslatef(0.05 - i * 0.025, -0.05, 0.2)
        glRotatef(-90, 1, 0, 0)
        create_cylinder(0.01, 0.001, 0.04, 8, 1)
        glPopMatrix()

def render_scales(base_color):
    scale_color = [max(0, c - 0.2) for c in base_color]  # Darken the scale color
    set_material(*scale_color)
    
    radius = 0.5  # Radius of the dragon's body
    for phi in range(0, 180, 15):  # Angle from top to bottom
        for theta in range(0, 360, 15):  # Angle around the body
            phi_rad = math.radians(phi)
            theta_rad = math.radians(theta)
            
            x = radius * math.sin(phi_rad) * math.cos(theta_rad)
            y = radius * math.sin(phi_rad) * math.sin(theta_rad)
            z = radius * math.cos(phi_rad)
            
            glPushMatrix()
            glTranslatef(x, y, z)
            
            # Orient the scale to face outward
            glNormal3f(x, y, z)
            up = [0, 0, 1]
            right = [y, -x, 0]
            look_at = [x, y, z]
            
            glMultMatrixf([right[0], right[1], right[2], 0,
                           up[0], up[1], up[2], 0,
                           look_at[0], look_at[1], look_at[2], 0,
                           0, 0, 0, 1])
            
            # Render individual scale
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0, 0, 0)
            for i in range(7):
                angle = i * 2 * math.pi / 6
                glVertex3f(0.05 * math.cos(angle), 0.05 * math.sin(angle), 0)
            glEnd()
            
            glPopMatrix()

def render_hostile_dragon():
    glPushMatrix()
    
    base_color = (0.9, 0.2, 0.2)  # Brighter red
    
    # Body
    # set_material(*base_color)
    set_material(*base_color)
    create_sphere(0.5, 32, 32)
    render_scales(base_color)
    
    # Neck
    glPushMatrix()
    glTranslatef(0, 0, 0.4)
    glRotatef(-30, 1, 0, 0)
    # set_material(*base_color)
    set_material(*base_color)
    create_cylinder(0.2, 0.15, 0.6, 16, 8)
    glPushMatrix()
    glScale(0.4, 0.4, 1.2)
    render_scales(base_color)
    glPopMatrix()
    
    # Head
    glTranslatef(0, 0, 0.6)
    # set_material(*base_color)
    set_material(*base_color)
    create_sphere(0.25, 32, 32)
    render_teeth()
    
    # Eyes
    glPushMatrix()
    glTranslatef(0.15, 0.2, 0.2)
    set_material(1.0, 0.7, 0.0)  # Amber eyes
    create_sphere(0.08, 16, 16)
    # Pupil
    glPushMatrix()
    glTranslatef(0, 0, 0.06)
    set_material(0.0, 0.0, 0.0)  # Black pupil
    create_sphere(0.04, 12, 12)
    glPopMatrix()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.15, 0.2, 0.2)
    set_material(1.0, 0.7, 0.0)  # Amber eyes
    create_sphere(0.08, 16, 16)
    # Pupil
    glPushMatrix()
    glTranslatef(0, 0, 0.06)
    set_material(0.0, 0.0, 0.0)  # Black pupil
    create_sphere(0.04, 12, 12)
    glPopMatrix()
    glPopMatrix()
    
    # Horns
    set_material(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0.1, 0.15, 0)
    glRotatef(30, 0, 0, 1)
    glRotatef(-20, 1, 0, 0)
    create_cylinder(0.05, 0.01, 0.3, 8, 4)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-0.1, 0.15, 0)
    glRotatef(-30, 0, 0, 1)
    glRotatef(-20, 1, 0, 0)
    create_cylinder(0.05, 0.01, 0.3, 8, 4)
    glPopMatrix()
    
    glPopMatrix()  # End of head and neck
    
    # Wings
    glPushMatrix()
    glTranslatef(0.4, 0, 0)
    glRotatef(110, 0, 1, 0)
    glRotatef(-10, 1, 0, 0)
    create_wing(1.2, 16, 0.7, 0.3, 0.3, 0.7)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.4, 0, 0)
    glRotatef(-110, 0, 1, 0)
    glRotatef(-10, 1, 0, 0)
    create_wing(1.2, 16, 0.7, 0.3, 0.3, 0.7)
    glPopMatrix()
    
    # Tail
    glPushMatrix()
    glTranslatef(0, -0.1, -0.5)
    glRotatef(20, 1, 0, 0)
    set_material(*base_color)
    create_cylinder(0.1, 0.01, 1.0, 16, 8)
    glTranslatef(0, 0, 1.0)
    glRotatef(20, 1, 0, 0)
    create_cylinder(0.05, 0.01, 0.5, 8, 4)
    glPopMatrix()
    
    glPopMatrix()

def render_friendly_dragon():
    glPushMatrix()
    
    base_color = (0.4, 0.6, 1.0)  # Brighter blue
    
    # Body
    # set_material(*base_color)
    set_material(*base_color)
    create_sphere(0.5, 32, 32)
    render_scales(base_color)
    
    # Neck
    glPushMatrix()
    glTranslatef(0, 0, 0.4)
    glRotatef(-45, 1, 0, 0)
    # set_material(*base_color)
    set_material(*base_color)
    create_cylinder(0.2, 0.15, 0.5, 16, 8)
    glPushMatrix()
    glScale(0.4, 0.4, 1.0)
    render_scales(base_color)
    glPopMatrix()
    
    # Head
    glTranslatef(0, 0, 0.5)
    # set_material(*base_color)
    set_material(*base_color)
    create_sphere(0.25, 32, 32)
    render_teeth()
    
    # Eyes
    glPushMatrix()
    glTranslatef(0.15, 0.2, 0.2)
    set_material(0.0, 1.0, 1.0)  # Bright cyan eyes
    create_sphere(0.08, 16, 16)
    # Pupil
    glPushMatrix()
    glTranslatef(0, 0, 0.06)
    set_material(0.0, 0.0, 0.0)  # Black pupil
    create_sphere(0.04, 12, 12)
    glPopMatrix()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.15, 0.2, 0.2)
    set_material(0.0, 1.0, 1.0)  # Bright cyan eyes
    create_sphere(0.08, 16, 16)
    # Pupil
    glPushMatrix()
    glTranslatef(0, 0, 0.06)
    set_material(0.0, 0.0, 0.0)  # Black pupil
    create_sphere(0.04, 12, 12)
    glPopMatrix()
    glPopMatrix()
    
    # Crest
    set_material(0.7, 0.9, 1.0)
    glPushMatrix()
    glTranslatef(0, 0.2, -0.1)
    glRotatef(90, 1, 0, 0)
    create_cylinder(0.05, 0.01, 0.3, 8, 4)
    glPopMatrix()
    
    glPopMatrix()  # End of head and neck
    
    # Wings
    glPushMatrix()
    glTranslatef(0.4, 0, 0)
    glRotatef(100, 0, 1, 0)
    glRotatef(-20, 1, 0, 0)
    create_wing(1.5, 20, 0.6, 0.8, 1.0, 0.6)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.4, 0, 0)
    glRotatef(-100, 0, 1, 0)
    glRotatef(-20, 1, 0, 0)
    create_wing(1.5, 20, 0.6, 0.8, 1.0, 0.6)
    glPopMatrix()
    
    # Tail
    glPushMatrix()
    glTranslatef(0, -0.1, -0.5)
    glRotatef(10, 1, 0, 0)
    set_material(*base_color)
    create_cylinder(0.1, 0.05, 1.2, 16, 8)
    glTranslatef(0, 0, 1.2)
    glRotatef(30, 1, 0, 0)
    create_cylinder(0.05, 0.01, 0.6, 8, 4)
    glPopMatrix()
    
    glPopMatrix()

friendly_dragon_list = None
hostile_dragon_list = None

def create_dragon_display_lists():
    global friendly_dragon_list, hostile_dragon_list
    friendly_dragon_list = glGenLists(1)
    glNewList(friendly_dragon_list, GL_COMPILE)
    render_friendly_dragon()
    glEndList()

    hostile_dragon_list = glGenLists(1)
    glNewList(hostile_dragon_list, GL_COMPILE)
    render_hostile_dragon()
    glEndList()