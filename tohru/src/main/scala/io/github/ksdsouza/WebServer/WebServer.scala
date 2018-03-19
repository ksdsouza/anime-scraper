package io.github.ksdsouza.WebServer



import java.util.Properties

import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.stream.ActorMaterializer
import org.mongodb.scala.MongoClient

import scala.io.StdIn

object MainRouter {
  val routes = GetRouter.route
}



object WebServer {
  val client = MongoClient("mongodb://localhost:27017")

  def main(args: Array[String]) {
    implicit val system = ActorSystem("my-system")

    def onComplete(): Unit ={
      client.close()
      system.terminate()
    }

    implicit val materializer = ActorMaterializer()
    // needed for the future flatMap/onComplete in the end
    implicit val executionContext = system.dispatcher

    val properties = new Properties()
    properties.load(getClass.getResourceAsStream("Server.properties"))
    val url = properties.getProperty("url")
    val port = properties.getProperty("port").toInt

    val bindingFuture = Http().bindAndHandle(MainRouter.routes, url, port)

    println(s"Server online at http://$url:$port/\nPress RETURN to stop...")
    StdIn.readLine() // let it run until user presses return
    bindingFuture
      .flatMap(_.unbind()) // trigger unbinding from the port
      .onComplete(_ => onComplete()) // and shutdown when done
  }
}