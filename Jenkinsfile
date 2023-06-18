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

        def excludeStatic = fileExists('static') ? "-x static/*" : ""
        def excludeMedia = fileExists('media') ? "-x media/*" : ""

        stage('Backup Existing Project') {
            steps {
                // Backup the existing project by zip it to /var/www/backup
                sh "zip -r /var/www/backup/pms_backend_${BUILD_NUMBER}.zip /var/www/pms_backend $exclude_static $exclude_media"
                sh "chmod 755 /var/www/backup/pms_backend_${BUILD_NUMBER}.zip"
            }
        }

        stage('Zip and deploy new code') {
            steps {
                // Zip the new code from jenkins workspace
                sh "cd ${WORKSPACE} && zip -r /var/www/allCodes/pms_backend_${BUILD_NUMBER}.zip . $exclude_static $exclude_media"
                sh "chmod 755 /var/www/allCodes/pms_backend_${BUILD_NUMBER}.zip"

                // Unzip those new code
                sh "unzip -q /var/www/allCodes/pms_backend_${BUILD_NUMBER}.zip -d /var/www/pms_backend $exclude_static $exclude_media"
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
