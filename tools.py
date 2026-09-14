# tools.py

# Tools used by Raseen AI Maintenance Agent

def reduce_motor_speed_api(current_rpm, reduction_percent=30):

    """

    Simulates an autonomous action that reduces motor speed.

    """

    reduction = current_rpm * (reduction_percent / 100)

    new_rpm = int(current_rpm - reduction)

    return {

        "success": True,

        "action": "reduce_motor_speed",

        "old_rpm": current_rpm,

        "new_rpm": new_rpm,

        "reduction_percent": reduction_percent,

        "message": f"Motor speed reduced from {current_rpm} RPM to {new_rpm} RPM."

    }

def create_work_order_api(priority="HIGH", equipment="Motor-01"):

    """

    Simulates creating a maintenance work order.

    """

    work_order_id = "WO-1001"

    return {

        "success": True,

        "action": "create_work_order",

        "work_order_id": work_order_id,

        "equipment": equipment,

        "priority": priority,

        "status": "CREATED",

        "message": f"Maintenance work order {work_order_id} created with {priority} priority."

    }
