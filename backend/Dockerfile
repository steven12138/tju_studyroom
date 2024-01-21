# 使用带有 Maven 和 Java 18 的官方镜像作为构建基础
FROM maven:3.8.7-openjdk-18 as BUILD

WORKDIR /build

COPY pom.xml /build/

RUN mvn dependency:go-offline

COPY src /build/src

RUN mvn clean package -DskipTests -Pprod

FROM openjdk:17-slim

WORKDIR /app
COPY --from=BUILD /build/target/*.jar /app/app.jar
COPY application-prod.yaml /app/application.yaml
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/app/app.jar"]