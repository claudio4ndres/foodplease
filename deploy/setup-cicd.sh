#!/bin/bash
# Configura en AWS lo necesario para el pipeline de GitHub Actions (una sola vez).
# Ejecutar en CloudShell de la consola AWS (ya autenticada).
#  1) Rol IAM para que la instancia EC2 se registre en SSM.
#  2) Proveedor OIDC de GitHub (confianza federada, sin credenciales guardadas).
#  3) Rol que GitHub Actions asume, limitado a ordenar el despliegue en esta instancia.
set -e

CUENTA=912644496587
REGION=us-east-2
INSTANCIA=i-0f30255f21806b764
REPO=claudio4ndres/foodplease

echo "== 1. Rol SSM para la instancia =="
aws iam create-role --role-name foodplease-ec2-ssm \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}' 2>/dev/null || echo "(rol ya existia)"
aws iam attach-role-policy --role-name foodplease-ec2-ssm \
  --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
aws iam create-instance-profile --instance-profile-name foodplease-ec2-ssm 2>/dev/null || echo "(perfil ya existia)"
aws iam add-role-to-instance-profile --instance-profile-name foodplease-ec2-ssm --role-name foodplease-ec2-ssm 2>/dev/null || echo "(ya asociado)"
sleep 10
aws ec2 associate-iam-instance-profile --region $REGION --instance-id $INSTANCIA \
  --iam-instance-profile Name=foodplease-ec2-ssm 2>/dev/null || echo "(instancia ya tenia perfil)"

echo "== 2. Proveedor OIDC de GitHub =="
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com 2>/dev/null || echo "(proveedor ya existia)"

echo "== 3. Rol para GitHub Actions =="
cat > /tmp/confianza.json <<JSON
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::${CUENTA}:oidc-provider/token.actions.githubusercontent.com" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
      "StringLike": { "token.actions.githubusercontent.com:sub": "repo:${REPO}:ref:refs/heads/main" }
    }
  }]
}
JSON
aws iam create-role --role-name foodplease-github-deploy \
  --assume-role-policy-document file:///tmp/confianza.json 2>/dev/null || \
aws iam update-assume-role-policy --role-name foodplease-github-deploy \
  --policy-document file:///tmp/confianza.json

cat > /tmp/permisos.json <<JSON
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ssm:SendCommand",
      "Resource": [
        "arn:aws:ssm:${REGION}::document/AWS-RunShellScript",
        "arn:aws:ec2:${REGION}:${CUENTA}:instance/${INSTANCIA}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["ssm:GetCommandInvocation", "ssm:ListCommands"],
      "Resource": "*"
    }
  ]
}
JSON
aws iam put-role-policy --role-name foodplease-github-deploy \
  --policy-name desplegar-por-ssm --policy-document file:///tmp/permisos.json

echo "== 4. Reiniciar la instancia para que el agente SSM tome el rol =="
aws ec2 reboot-instances --region $REGION --instance-ids $INSTANCIA

echo ""
echo "Listo. En ~3 minutos la instancia deberia aparecer registrada en SSM:"
echo "  aws ssm describe-instance-information --region $REGION --query 'InstanceInformationList[].InstanceId'"
