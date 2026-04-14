import anchorpoint as ap
import apsync

# Get the current context
ctx = ap.get_context()
ui = ap.UI()

try:
    # Check if we're in a project
    if not ctx.project_id or not ctx.workspace_id:
        ui.show_error("Error", "This action can only be run within a project")
        print("Error: Not in a project context")
    else:
        # Get all project members
        print(f"Retrieving project members for project: {ctx.project_id}")
        members = apsync.get_project_members(ctx.workspace_id, ctx.project_id)
        
        # Extract user IDs
        user_ids = [member.id for member in members]
        print(f"Found {len(user_ids)} project members: {user_ids}")
        
        # Create test metadata
        metadata = {
            "test_type": "custom_notification_test",
            "sender": ctx.username,
            "timestamp": "2026-03-24",
            "priority": "high",
            "workflow": "testing",
            "project_path": ctx.path,
            "custom_data": "This is a test notification!",
            "number_value": 42,
            "boolean_flag": True
        }
        
        print(f"Sending notification with metadata: {metadata}")
        
        # Send the custom notification to all project members
        ap.schedule_custom_notification(
            ctx.project_id,
            ctx.workspace_id,
            "Test notification from Anchorpoint Action",
            user_ids,
            metadata
        )
        
        ui.show_success("Notification Sent", f"Test notification sent to {len(user_ids)} project members")
        print(f"Successfully sent custom notification to {len(user_ids)} users")

except Exception as e:
    error_message = f"Failed to send notification: {str(e)}"
    ui.show_error("Error", error_message)
    print(error_message)
    import traceback
    traceback.print_exc()
