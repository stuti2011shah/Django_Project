import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Tags, User

def recommend_users(user, n=5):
    """
    Recommends users based on tags using an AI model.
    Args:
    user (User): The user for whom recommendations are being made.
    n (int, optional): The number of recommended users to return. Defaults to 5.
    Returns:
    list: A list of recommended User objects.
    """
    try:
        # Get user tags
        user_tags = Tags.objects.filter(coder=user)
        if not user_tags:
            return []  # No tags available for the user
        
        user_tags_name = [tag.name for tag in user_tags]
        user_tag_string = ' '.join(user_tags_name)
        
        # Query all other users
        users = User.objects.exclude(id=user.id)
        user_tags_dict = {}
        for user in users:
            tags = Tags.objects.filter(coder=user)
            users_tags_name = [tag.name for tag in tags]
            tag_string = ' '.join(users_tags_name)
            user_tags_dict[user.id] = tag_string
        
        if not user_tags_dict:
            return []  # No other users to recommend

        # Create dataframe of users and tags
        user_tag_df = pd.DataFrame(list(user_tags_dict.items()), columns=['user_id', 'tags'])
        
        # Vectorize tags
        vectorizer = CountVectorizer()
        tag_vectors = vectorizer.fit_transform(user_tag_df['tags'])
        user_tag_vector = vectorizer.transform([user_tag_string])
        
        # Calculate cosine similarity matrix
        cosine_similarities = cosine_similarity(user_tag_vector, tag_vectors)[0]
        
        # Sort users by similarity score
        similar_user_indices = cosine_similarities.argsort()[::-1]
        similar_users = user_tag_df.iloc[similar_user_indices]
        
        # Get top n recommended user IDs
        recommended_user_ids = similar_users.head(n)['user_id'].tolist()
        
        recommend_users = [User.objects.get(id=i) for i in recommended_user_ids]
        return recommend_users
    
    except Exception as e:
        # Log or print the exception for debugging
        print(f"Error recommending users: {e}")
        return []
