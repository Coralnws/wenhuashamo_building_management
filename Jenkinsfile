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
                    sh "cd ${WORKSPACE} && zip -r /var/www/allCodes/pms_backend_${BUILD_NUMBER}.zip ."
                    sh "chmod 755 /var/www/allCodes/pms_backend_${BUILD_NUMBER}.zip"

                    // Unzip the new code to /var/www/pms_backend
                    sh "unzip -qo /var/www/allCodes/pms_backend_${BUILD_NUMBER}.zip -d /var/www/pms_backend"
                }
            }
        }

        // This stage is needed when want to rebuild the docker image
        // example: need to run the Dockerfile (i.e: run pip install and so on)
        stage('Build and Deploy Docker Container') {
            steps {
                // Build the Docker image
                sh "docker build -t pms_backend:${BUILD_NUMBER} /var/www/pms_backend"

                // Stop the existing container
                sh "docker stop pms_backend || true"
                sh "docker rm pms_backend || true"

                // Run the new container
                sh "docker run -d -p 8000:8000 -v /var/www/pms_backend:/code --name pms_backend pms_backend:${BUILD_NUMBER}"
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    sh """
                        /var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQube/bin/sonar-scanner \
                        -Dsonar.login=dd13ebb79932f3b100f79a1d492482175a126636 \
                        -Dsonar.projectKey=prj_2023_group11_pms_backend \
                        -Dsonar.projectName=prj_2023_group11_pms_backend \
                        -Dsonar.host.url=http://10.134.136.70:9000 \
                        -Dsonar.sources=/var/lib/jenkins/workspace/pms_backend_docker_pipline \
                        -Dsonar.projectBaseDir=/var/lib/jenkins/workspace/pms_backend_docker_pipline \
                        -Dsonar.exclusions=**/static/**, **/tests/**, **/venv/**, **/migrations/** \
                    """
                }
            }
        }
    }
}
