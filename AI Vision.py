'''

**PLEASE DO NOT COPY THIS DOCSTRING**

1) Replace key = your key in RG1->name-of-model->keys
2) Do the same for Endpoint
3) IMPORTANT: Install azure.ai.vision by the following promt:"{ pip install azure.ai.vision }" in new terminal.
  (IT WILL BE ALREADY INSTALLED ON THE VM)
4) Rest is already solved, you just need to refer to this and run the code.
5) If error shows up like sample.jpg not found, please wait for 2-3 min and do the process again.
6) Submit Assessment

'''

import azure.ai.vision as visionsdk

key = "REPLACE-WITH-YOUR-VALUE"
endpoint = "REPLACE-WITH-YOUR-VALUE"

def AnalyzeImage(endpoint: str, key: str) -> None:
    service_options = visionsdk.VisionServiceOptions(endpoint, key)

    ''' Specify the image file on disk to analyze. sample.jpg is a good example to show most features'''
    vision_source = visionsdk.VisionSource(filename=r"sample.jpg")
    analysis_options = visionsdk.ImageAnalysisOptions()
    analysis_options.features = (
        visionsdk.ImageAnalysisFeature.OBJECTS |
        visionsdk.ImageAnalysisFeature.PEOPLE |
        visionsdk.ImageAnalysisFeature.TEXT |
        visionsdk.ImageAnalysisFeature.TAGS
    )

    image_analyzer = visionsdk.ImageAnalyzer(service_options, vision_source, analysis_options)

    print("Please wait for image analysis results...")
    result = image_analyzer.analyze()

    # Checks result.
    if result.reason == visionsdk.ImageAnalysisResultReason.ANALYZED:
        if result.objects is not None:
            print("Objects:")
            for object in result.objects:
                print("   '{}', {}, Confidence: {:.4f}".format(object.name, object.bounding_box, object.confidence))

        if result.tags is not None:
            print("Tags:")
            for tag in result.tags:
                '''point 3 write your code here'''
                print("   '{}', Confidence {:.4f}".format(tag.name, tag.confidence))

        if result.people is not None:
            print("People:")
            for person in result.people:
                '''point 4 write your code here'''
                if tag.confidence >= 0.90:
                    print("   {}, Confidence {:.4f}".format(person.bounding_box, person.confidence))

        if result.text is not None:
            print("Text:")
            for line in result.text.lines:
                points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
                print("   Line: '{}', Bounding polygon {}".format(line.content, points_string))

                for word in line.words:
                    points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                    print("     Word: '{}', Bounding polygon {}, Confidence {:.4f}".format(word.content, points_string, word.confidence))
    else:
        error_details = visionsdk.ImageAnalysisErrorDetails.from_result(result)
        print("Analysis failed.")
        print("   Error reason: {}".format(error_details.reason))
        print("   Error code: {}".format(error_details.error_code))
        print("   Error message: {}".format(error_details.message))
        print("Did you set the computer vision endpoint and key?")

AnalyzeImage(endpoint, key)