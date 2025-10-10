"""
Analytics and progress tracking module
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class ProgressTracker:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_user_dashboard_stats(self, user_id):
        """Get comprehensive dashboard statistics for a user"""
        stats = self.db.get_user_statistics(user_id)
        
        return {
            'total_questions': stats['total_questions'],
            'correct_answers': stats['correct_answers'],
            'overall_accuracy': round(stats['accuracy'], 1),
            'system_performance': stats['system_performance']
        }
    
    def create_performance_chart(self, user_id):
        """Create a performance chart by system"""
        stats = self.db.get_user_statistics(user_id)
        system_perf = stats['system_performance']
        
        if not system_perf:
            return None
        
        # Prepare data
        systems = list(system_perf.keys())
        accuracies = [system_perf[s]['accuracy'] for s in systems]
        totals = [system_perf[s]['total'] for s in systems]
        
        # Create bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=systems,
            y=accuracies,
            text=[f"{acc:.1f}%" for acc in accuracies],
            textposition='auto',
            marker_color='#28A745',
            hovertemplate='<b>%{x}</b><br>Accuracy: %{y:.1f}%<br>Questions: %{customdata}<extra></extra>',
            customdata=totals
        ))
        
        fig.update_layout(
            title="Performance by System",
            xaxis_title="System",
            yaxis_title="Accuracy (%)",
            yaxis_range=[0, 100],
            template="plotly_white",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def identify_weak_areas(self, user_id, threshold=70):
        """Identify systems where user performance is below threshold"""
        stats = self.db.get_user_statistics(user_id)
        system_perf = stats['system_performance']
        
        weak_areas = []
        for system, perf in system_perf.items():
            if perf['accuracy'] < threshold and perf['total'] >= 5:  # At least 5 questions
                weak_areas.append({
                    'system': system,
                    'accuracy': perf['accuracy'],
                    'questions_answered': perf['total']
                })
        
        # Sort by accuracy (lowest first)
        weak_areas.sort(key=lambda x: x['accuracy'])
        
        return weak_areas
    
    def get_study_recommendations(self, user_id):
        """Get personalized study recommendations"""
        weak_areas = self.identify_weak_areas(user_id)
        
        recommendations = []
        
        if weak_areas:
            for area in weak_areas[:3]:  # Top 3 weak areas
                recommendations.append({
                    'type': 'weak_area',
                    'system': area['system'],
                    'message': f"Focus on {area['system']} - Current accuracy: {area['accuracy']:.1f}%",
                    'priority': 'high'
                })
        else:
            recommendations.append({
                'type': 'general',
                'message': "Great job! Continue practicing across all systems to maintain your performance.",
                'priority': 'normal'
            })
        
        return recommendations
