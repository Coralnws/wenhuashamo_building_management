pipeline {
    agent any

    environment {
        // Global credential in jenkins (id)
        GIT_CREDENTIALS = credentials('kaiba-tencent-git-token')
    }

    stages {

        // ++++++++++++++++++++
        //  NOTE: BECAUSE USING PIPELINE WITH SCM AND ALREADY ADDED REPO,
        //  SO NO NEED TO EXPLICITLY PULL CODE FROM GIT AGAIN,
        //  HENCE FIRST STEP (THIS STAGE) CAN OMIT
        // ++++++++++++++++++++
        // stage('Clone Git Repository') {
        //     steps {
        //         git credentialsId: "${GIT_CREDENTIALS}", url: 'https://git.code.tencent.com/8c49d71dc01e57667266b1bd940a74d6/9e17722788468ca58ad1bd54fba657b1/pms_backend.git'
        //     }
        // }

        stage('Backup Existing Project') {
            steps {
                script {
                    def excludeStatic = fileExists('static') ? "-x static/" : ""
                    def excludeMedia = fileExists('media') ? "-x media/" : ""

                    // Backup the existing project by zipping it to /var/www/backup
                    sh "zip -r /var/www/backup/pms_backend_${BUILD_NUMBER}.zip /var/www/pms_backend $excludeStatic $excludeMedia"
                    sh "chmod 755 /var/www/backup/pms_backend_${BUILD_NUMBER}.zip"
                }
            }
        }

        stage('Zip and Deploy New Code') {
            steps {
                script {
                    // Zip the new code from Jenkins workspace
                    sh "cd ${WORKSPACE} && zip -r /var/www/allCodes/pms_backend_${BUILD_NUMBER}.zip . $excludeStatic $excludeMedia"
                    sh "chmod 755 /var/www/allCodes/pms_backend_${BUILD_NUMBER}.zip"

                    // Unzip the new code to /var/www/pms_backend
                    sh "unzip -qo /var/www/allCodes/pms_backend_${BUILD_NUMBER}.zip -d /var/www/pms_backend $excludeStatic $excludeMedia"
                }
            }
        }

        // This stage is needed when want to rebuild the docker image
        // example: need to run the Dockerfile (i.e: run pip install and so on)
        stage('Build and deploy Docker container') {
            steps {
                // Build the Docker image
                sh "docker build -t pms_backend:${BUILD_NUMBER} /var/www/pms_backend"

                // Stop the existing container
                sh "docker stop pms_backend || true"
                sh "docker rm pms_backend || true"

                // Run the new container
                sh "docker run -d -p 8000:8000 -v code:/var/www/pms_backend pms_backend:${BUILD_NUMBER}"
            }
        }
    }
}
