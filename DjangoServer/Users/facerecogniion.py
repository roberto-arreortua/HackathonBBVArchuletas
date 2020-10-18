import boto3

def compare_faces(sourceFile, targetFile):
    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=80,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
              str(position['Left']) + ' ' +
              str(position['Top']) +
              ' matches with ' + similarity + '% confidence')

    imageSource.close()
    imageTarget.close()
    return len(response['FaceMatches'])


def start(source_file,target_file):
    print(source_file,target_file)
    #source_file = 'Person_1/person22.jpg'
    #target_file = 'Person_1/person2.jpg'
    face_matches = compare_faces(source_file, target_file)
    print("Face matches: " + str(face_matches))

    if face_matches == 0:
        value = False
    elif face_matches >= 1:
        value = True

    return (value)


