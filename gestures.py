import math

# GEOMETRY
def distance(p1, p2):
    #Calculate 3D distance between two landmarks.

    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dz = p1.z - p2.z

    return math.sqrt(dx * dx + dy * dy + dz * dz)


def angle(a, b, c):

     
   
    ba = (
        a.x - b.x,
        a.y - b.y,
        a.z - b.z
    )

    bc = (
        c.x - b.x,
        c.y - b.y,
        c.z - b.z
    )

    dot_product = (
        ba[0] * bc[0]
        + ba[1] * bc[1]
        + ba[2] * bc[2]
    )

    magnitude_ba = math.sqrt(
        ba[0] ** 2
        + ba[1] ** 2
        + ba[2] ** 2
    )

    magnitude_bc = math.sqrt(
        bc[0] ** 2
        + bc[1] ** 2
        + bc[2] ** 2
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0

    cosine = dot_product / (
        magnitude_ba * magnitude_bc
    )

    cosine = max(-1.0, min(1.0, cosine))

    return math.degrees(
        math.acos(cosine)
    )

# FINGER DETECTION

def is_finger_extended(landmarks, mcp, pip, dip, tip):
    

    mcp_angle = angle(
        landmarks[0],
        landmarks[mcp],
        landmarks[pip]
    )

    pip_angle = angle(
        landmarks[mcp],
        landmarks[pip],
        landmarks[dip]
    )

    dip_angle = angle(
        landmarks[pip],
        landmarks[dip],
        landmarks[tip]
    )

    # A reasonably straight finger has large joint angles.
    return (
        mcp_angle > 150
        and pip_angle > 150
        and dip_angle > 140
    )

# THUMB DETECTION
 
def is_thumb_extended(landmarks):
    

    thumb_cmc = landmarks[1]
    thumb_mcp = landmarks[2]
    thumb_ip = landmarks[3]
    thumb_tip = landmarks[4]

    # Thumb should be relatively straight.
    thumb_angle = angle(
        thumb_mcp,
        thumb_ip,
        thumb_tip
    )

    # Thumb tip should be sufficiently far from the wrist / palm area.
    tip_distance = distance(
        thumb_tip,
        landmarks[0]
    )

    mcp_distance = distance(
        thumb_mcp,
        landmarks[0]
    )

    return (
        thumb_angle > 145
        and tip_distance > mcp_distance * 1.15
    )


 

def is_thumb_up(landmarks):
    

    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    thumb_mcp = landmarks[2]

    # 1. Thumb must point upward

    thumb_points_up = (
        thumb_tip.y < thumb_ip.y
        and thumb_ip.y < thumb_mcp.y
    )

    # 2. Thumb should be reasonably straight

    thumb_angle = angle(
        thumb_mcp,
        thumb_ip,
        thumb_tip
    )

    thumb_is_straight = thumb_angle > 120

     
    # 3. THUMB UP

    index_mcp = landmarks[5]

    thumb_is_above_palm = (
        thumb_tip.y < index_mcp.y - 0.05
    )

    # Thumb tip must be sufficiently away from the wrist.
 
    wrist = landmarks[0]

    thumb_wrist_distance = distance(
        thumb_tip,
        wrist
    )

    palm_distance = distance(
        index_mcp,
        wrist
    )

    thumb_is_extended = (
        thumb_wrist_distance > palm_distance * 1.20
    )

    return (
        thumb_points_up
        and thumb_is_straight
        and thumb_is_above_palm
        and thumb_is_extended
    )


 
    #  THUMB DOWN  
 

def is_thumb_down(landmarks):
    """
    Detect a thumb-down gesture.

    Thumb tip should be below the thumb IP joint,
    while the thumb remains reasonably straight.
    """

    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    thumb_mcp = landmarks[2]

    # Thumb should point downward.
    thumb_points_down = (
        thumb_tip.y > thumb_ip.y
        and thumb_ip.y > thumb_mcp.y
    )

    # Thumb should still be reasonably straight.
    thumb_angle = angle(
        thumb_mcp,
        thumb_ip,
        thumb_tip
    )

     
    # This prevents a folded thumb from being classified as THUMB_DOWN.
 
    thumb_distance = distance(
        thumb_tip,
        landmarks[0]
    )

    palm_size = distance(
        landmarks[9],
        landmarks[0]
    )

    thumb_is_extended = (
        thumb_distance > palm_size * 1.05
    )

    return (
        thumb_points_down
        and thumb_angle > 120
        and thumb_is_extended
    )


 
# FINGER STATES
 
def get_finger_states(landmarks):
    """
    Return the open/closed state of all five fingers.
    """

    states = {}

   
    # Thumb

    states["thumb"] = is_thumb_extended(
        landmarks
    )

    # Index
 
    states["index"] = is_finger_extended(
        landmarks,
        5,
        6,
        7,
        8
    )

    # Middle
 
    states["middle"] = is_finger_extended(
        landmarks,
        9,
        10,
        11,
        12
    )

    # Ring
 
    states["ring"] = is_finger_extended(
        landmarks,
        13,
        14,
        15,
        16
    )

    # Pinky
 
    states["pinky"] = is_finger_extended(
        landmarks,
        17,
        18,
        19,
        20
    )

    return states


# GESTURE RECOGNITION
 
def recognize_gesture(landmarks):
    """
    Recognize basic static gestures.
    """

    fingers = get_finger_states(landmarks)

    thumb = fingers["thumb"]
    index = fingers["index"]
    middle = fingers["middle"]
    ring = fingers["ring"]
    pinky = fingers["pinky"]

    # OPEN PALM
 
    if (
        thumb
        and index
        and middle
        and ring
        and pinky
    ):
        return "OPEN_PALM"

    # THUMB UP
 
    if (
        not index
        and not middle
        and not ring
        and not pinky
        and is_thumb_up(landmarks)
    ):
        return "THUMB_UP"

    # THUMB DOWN
 
    if (
        not index
        and not middle
        and not ring
        and not pinky
        and is_thumb_down(landmarks)
    ):
        return "THUMB_DOWN"

    # INDEX
 
    if (
        index
        and not middle
        and not ring
        and not pinky
    ):
        return "INDEX"

    # TWO FINGERS
 
    if (
        index
        and middle
        and not ring
        and not pinky
    ):
        return "TWO_FINGERS"

    # THREE FINGERS
 
    if (
        index
        and middle
        and ring
        and not pinky
    ):
        return "THREE_FINGERS"

    # UNKNOWN
 
    return "UNKNOWN GESTURE"