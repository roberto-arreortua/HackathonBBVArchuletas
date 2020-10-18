const multer = require('multer');
const fs = require('fs');

var enrollWav;
var enrollMap = new Map();
var verifyWav;
var verifyMap = new Map();

const enrollVoice = (req, res) => {
    const storage = multer.memoryStorage();
    const upload = multer({
        storage: storage,
        limits: {
            fields: 1,
            fileSize: 6000000,
            files: 1,
            parts: 2
        }
    });
    // 'audio' and 'name' in body form-data
    upload.single('audio')(req, res, (err) => {
        if (err) {
            console.log(err);
            return res.status(400).json({ Message: 'Error E' });
        } else if (!req.body.name) {
            return res.status(400).json({ Message: 'Invalid E' });
        }
        fs.writeFile('src/controllers/enrollWav_' + req.params.customerId + '.wav', req.file.buffer, function (err) {
            if (err) return console.log(err);
        });
        console.log('');
        return res.status(200).json({
            Message: 'Enrolled'
        });
    });
};

const verifyVoice = async (req, res) => {
    if (!fs.existsSync('src/controllers/enrollWav_' + req.params.customerId + '.wav')) {
        if (fs.existsSync('src/controllers/verifyWav_' + req.params.customerId + '.wav')) {
            fs.unlink('src/controllers/verifyWav_' + req.params.customerId + '.wav', function (err) {
                if (err) console.log(err);
            });
        }
        return res.status(400).json({ Message: 'Enrolled voice not found' });
    }
    const storage = multer.memoryStorage();
    const upload = multer({
        storage: storage,
        limits: {
            fields: 1,
            fileSize: 6000000,
            files: 1,
            parts: 2
        }
    });
    // 'audio' and 'name' in body form-data
    upload.single('audio')(req, res, (err) => {
        if (err) {
            console.log(err);
            return res.status(400).json({ Message: 'Error V' });
        } else if (!req.body.name) {
            return res.status(400).json({ Message: 'Invalid V' });
        }
        fs.writeFile('src/controllers/verifyWav_' + req.params.customerId + '.wav', req.file.buffer, function (err) {
            if (err) return console.log(err);
        });
        console.log('');
        (function () {
            "use strict";
            var sdk = require("microsoft-cognitiveservices-speech-sdk");
            var fs = require("fs");
            let getAudioConfigFromFile = (file) => {
                let pushStream = sdk.AudioInputStream.createPushStream();
                fs.createReadStream(file).on("data", function (arrayBuffer) {
                    pushStream.write(arrayBuffer.buffer);
                }).on("end", function () {
                    pushStream.close();
                });
                return sdk.AudioConfig.fromStreamInput(pushStream);
            };
            let subscriptionKey = "b1148f70abc04919962f5d4874db603d";
            let serviceRegion = "eastus";
            let enrollFile = "src/controllers/enrollWav_" + req.params.customerId + ".wav";
            let identificationFile = "src/controllers/verifyWav_" + req.params.customerId + ".wav";
            let speechConfig = sdk.SpeechConfig.fromSubscription(subscriptionKey, serviceRegion);
            let client = new sdk.VoiceProfileClient(speechConfig);
            let locale = "en-us";
            client.createProfileAsync(
                sdk.VoiceProfileType.TextIndependentIdentification,
                locale,
                function (result) {
                    let profile = result;
                    let enrollConfig = getAudioConfigFromFile(enrollFile);
                    console.log("Now enrolling voice from: " + enrollFile);
                    client.enrollProfileAsync(
                        profile,
                        enrollConfig,
                        function (enrollResult) {
                            console.log("(Enrollment result) Reason: " + sdk.ResultReason[enrollResult.reason]);
                            let identificationConfig = getAudioConfigFromFile(identificationFile);
                            let recognizer = new sdk.SpeakerRecognizer(speechConfig, identificationConfig);
                            let model = sdk.SpeakerIdentificationModel.fromProfiles([profile]);
                            recognizer.recognizeOnceAsync(
                                model,
                                function (identificationResult) {
                                    let reason = identificationResult.reason;
                                    console.log("(Identification result) Reason: " + sdk.ResultReason[reason]);
                                    if (reason === sdk.ResultReason.Canceled) {
                                        let cancellationDetails = sdk.SpeakerRecognitionCancellationDetails.fromResult(identificationResult);
                                        console.log("(Identification canceled) Error Details: " + cancellationDetails.errorDetails);
                                        console.log("(Identification canceled) Error Code: " + cancellationDetails.errorCode);
                                    } else {
                                        //console.log("(Identification result) Profile Id: " + identificationResult.profileId);
                                        console.log("(Identification result) Score: " + identificationResult.score);
                                    }
                                    client.deleteProfileAsync(
                                        profile,
                                        function (deleteResult) {
                                            console.log("(Delete profile result) Reason: " + sdk.ResultReason[deleteResult.reason]);
                                            fs.unlink('src/controllers/verifyWav_' + req.params.customerId + '.wav', function (err) {
                                                if (err) console.log(err);
                                            });
                                            fs.unlink('src/controllers/enrollWav_' + req.params.customerId + '.wav', function (err) {
                                                if (err) console.log(err);
                                            });
                                            console.log('Enroll and verify voice files for customer ' + req.params.customerId + ' deleted!');
                                            (function () {
                                                "use strict";
                                                var sdk2 = require("microsoft-cognitiveservices-speech-sdk");
                                                var fs2 = require("fs");
                                                var subscriptionKey2 = "b1148f70abc04919962f5d4874db603d";
                                                var serviceRegion2 = "eastus";
                                                fs2.writeFile('src/controllers/verifySpeechWav_' + req.params.customerId + '.wav', req.file.buffer, function (err2) {
                                                    if (err2) return console.log(err2);
                                                });
                                                var filename2 = 'src/controllers/verifySpeechWav_' + req.params.customerId + '.wav';
                                                var pushStream2 = sdk2.AudioInputStream.createPushStream();
                                                fs2.createReadStream(filename2).on('data', function (arrayBuffer) {
                                                    pushStream2.write(arrayBuffer.slice());
                                                }).on('end', function () {
                                                    pushStream2.close();
                                                });
                                                console.log("Now recognizing speech from: " + filename2);
                                                var audioConfig2 = sdk2.AudioConfig.fromStreamInput(pushStream2);
                                                var speechConfig2 = sdk2.SpeechConfig.fromSubscription(subscriptionKey2, serviceRegion2);
                                                speechConfig2.speechRecognitionLanguage = "es-MX";
                                                var recognizer2 = new sdk2.SpeechRecognizer(speechConfig2, audioConfig2);
                                                recognizer2.recognizeOnceAsync(
                                                    function (result) {
                                                        recognizer2.close();
                                                        recognizer2 = undefined;
                                                        fs2.unlink('src/controllers/verifySpeechWav_' + req.params.customerId + '.wav', function (err2) {
                                                            if (err2) console.log(err2);
                                                        });
                                                        console.log('Verify speech voice files for customer ' + req.params.customerId + ' deleted!');
                                                        console.log('Speech: ' + result.privText);
                                                        if (identificationResult.score > 0.49) {
                                                            return res.status(200).json({ Message: 'Granted', Confidence: identificationResult.score, Speech: result.privText });
                                                        } else {
                                                            return res.status(403).json({ Message: 'Denied', Confidence: identificationResult.score, Speech: result.privText });
                                                        }
                                                    },
                                                    function (err2) {
                                                        console.trace("err - " + err2);
                                                        recognizer2.close();
                                                        recognizer2 = undefined;
                                                        fs2.unlink('src/controllers/verifySpeechWav_' + req.params.customerId + '.wav', function (err) {
                                                            if (err) console.log(err);
                                                        });
                                                    });
                                            }());
                                        },
                                        function (err) {
                                            console.log("ERROR deleting profile: " + err);
                                        });
                                },
                                function (err) {
                                    console.log("ERROR recognizing speaker: " + err);
                                });
                        },
                        function (err) {
                            console.log("ERROR enrolling profile: " + err);
                        });
                },
                function (err) {
                    console.log("ERROR creating profile: " + err);
                });
        }());

    });
};

module.exports = { enrollVoice, verifyVoice, enrollMap, verifyMap };