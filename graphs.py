import matplotlib
matplotlib.use('Agg') # For server environment
import matplotlib.pyplot as plt
import os

def generate_activity_graph(logs, save_path="static/activity.png"):
    # Generate a simple bar chart of recent activities
    actions = {}
    for log in logs:
        actions[log.action] = actions.get(log.action, 0) + 1
        
    labels = list(actions.keys())
    values = list(actions.values())
    
    if not labels:
        labels = ["No Data"]
        values = [0]
        
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['#3b82f6', '#ef4444', '#f59e0b', '#10b981'][:len(labels)])
    plt.title('Moderation Activity')
    plt.ylabel('Count')
    
    # Ensure static directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    return save_path
