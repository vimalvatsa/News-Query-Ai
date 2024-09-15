# 🌟 News-Query-AI

Welcome to **News-Query-AI**, your intelligent companion for staying updated with the latest news! This innovative application leverages advanced AI technology to deliver the top news stories directly to you in a convenient Word document format. 

## 🗞️ Key Features

- **Real-Time News Updates**:  
  News-Query-AI continuously scans various reputable news sources to provide you with the most current and relevant news articles. You can trust that you are receiving the latest information at your fingertips.

- **User-Friendly Chatbot Interface**:  
  Interact with our intuitive chatbot to request news on specific topics or categories. Whether you're interested in politics, technology, sports, or entertainment, simply ask, and the chatbot will fetch the latest articles tailored to your interests.

- **Interactive Experience**:  
  Not only can you receive news updates, but you can also engage with the content. The chatbot allows you to ask follow-up questions, request summaries, or delve deeper into specific articles, making your news consumption more dynamic and personalized.

## ✅ Advantages

- **Efficiency**:  
  Save time by having the latest news compiled and delivered to you in a single document. No more endless scrolling through multiple websites; News-Query-AI does the heavy lifting for you.

- **Customization**:  
  Tailor your news experience by specifying your interests. The more you interact with the chatbot, the better it understands your preferences, ensuring that you receive news that matters most to you.

- **Accessibility**:  
  With news delivered in a Word document, you can easily save, share, or print articles for later reading, making it a versatile tool for both personal and professional use.

## 🚀 Getting Started

To run the News-Query-AI application on your local system, follow these steps:

### 1. Clone the Repository

First, clone the GitHub repository to your local machine:

```bash
git clone https://github.com/vimalvatsa/21BCE5888_ML.git
cd 21BCE5888_ML
```

### 2. Setup Redis Server

Before running the application, set up the Redis server for efficient caching:

```bash
# Pull the Redis image
docker pull redis

# Run the Redis container
docker run --name redis-server -d -p 6379:6379 redis
```

### 3. Build and Run with Docker

You can use Docker to build and run the application. Ensure you have Docker and Docker Compose installed on your system.

#### Build the Docker Image

Use the provided `Dockerfile` to build the image:

```bash
docker build -t 21BCE5888_ML .
```

#### Run the Application

Start the application using `docker-compose`:

```bash
docker-compose up
```

This command will start all the necessary services defined in the `docker-compose.yml` file, including the application and the vector databases -> etcd, Milvud and MinIO.

### 🌐 Accessing the Application

Once the services are up and running, you can interact with the News-Query-AI application through the chatbot interface (through POSTMAN API testing platform by running the URLS). The application will be accessible on the specified ports, allowing you to request the latest news and engage with the content.

---

Stay informed and engaged with **News-Query-AI**, where the latest news is just a chat away! 📰✨

