pipeline {
    agent any

    environment {
        SCRIPT = 'collect_configs.py'  // Your Python Paramiko script filename
        PATH = "${HOME}/.local/bin:${env.PATH}"
        PYTHONPATH = "${HOME}/.local/lib/python3.10/site-packages"
    }

    stages {
        stage('Install pip and Paramiko') {
            steps {
                sh '''
                    # Install pip if missing
                    if ! command -v pip3 > /dev/null; then
                        echo "[INFO] pip not found. Installing..."
                        wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
                        python3 get-pip.py --user
                    fi

                    # Upgrade pip and install paramiko
                    ~/.local/bin/pip3 install --user --upgrade pip
                    ~/.local/bin/pip3 install --user paramiko
                '''
            }
        }

        stage('Run Paramiko Script') {
            environment {
                CISCO_CREDS = credentials('cisco-ssh-creds')  // Jenkins credential ID
            }
            steps {
                sh '''
                    echo "[INFO] Executing Paramiko configuration collection script..."

                    export CISCO_CREDS_USR="${CISCO_CREDS_USR}"
                    export CISCO_CREDS_PSW="${CISCO_CREDS_PSW}"

                    python3 ${SCRIPT}
                '''
            }
        }
    }

    post {
        always {
            echo '[INFO] Archiving device outputs...'
            archiveArtifacts artifacts: '*_output.txt', allowEmptyArchive: true
        }
    }
}
