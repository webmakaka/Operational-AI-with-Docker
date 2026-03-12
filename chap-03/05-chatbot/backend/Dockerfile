FROM golang:1.22-alpine AS build
WORKDIR /app
COPY go.mod go.sum* ./
RUN go mod download || true
COPY . .
RUN go build -o backend .

FROM alpine:3.19
WORKDIR /app
COPY --from=build /app/backend .
EXPOSE 8080
CMD ["./backend"]
