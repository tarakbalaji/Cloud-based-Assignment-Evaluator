import boto3
from difflib import SequenceMatcher

# Set up AWS services
s3 = boto3.client('s3')
textract = boto3.client('textract')

# Set up similarity threshold
SIMILARITY_THRESHOLD = 0.0  # Adjust threshold as needed

def lambda_handler(event, context):
    # Get text from main file (test.pdf)
    main_file_bucket = 'newbucket1223211234312'
    main_file_key = 'test.pdf'
    main_file_text = extract_text_from_pdf(main_file_bucket, main_file_key)
    
    # Get text from sub file (t1.pdf)
    sub_file_bucket = 'newbucket1223211234312'
    sub_file_key = 't1.pdf'
    sub_file_text = extract_text_from_pdf(sub_file_bucket, sub_file_key)
    
    # Compare similarity of the two files
    similarity_score = calculate_similarity(main_file_text, sub_file_text)
    print("Similarity Score:", similarity_score)
    
    # Create response
    response = create_response(similarity_score)
    
    return response

def extract_text_from_pdf(bucket, key):
    response = textract.analyze_document(Document={'S3Object': {'Bucket': bucket, 'Name': key}}, FeatureTypes=['TABLES', 'FORMS'])

    text = ''
    # Extract text from Textract response
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE' and 'Text' in block:
            text += block['Text'] + ' '
    
    return text

def calculate_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

def create_response(similarity_score):
    similarity_percentage = similarity_score * 100
    body = f"Similarity Score: {similarity_percentage:.2f}%"
    
    return {
        'statusCode': 200,
        'body': body
    }

