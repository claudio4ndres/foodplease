#!/bin/bash
# Se ejecuta cuando LocalStack esta listo: crea los recursos AWS del proyecto
awslocal s3 mb s3://foodplease-fotos-platos
echo "Bucket S3 foodplease-fotos-platos creado en AWS local"
