package io.github.ksdsouza.WebServer

import akka.http.scaladsl.server.Directives._
import com.fasterxml.jackson.databind.ObjectMapper
import org.mongodb.scala.MongoClient

object GetRouter {
  val route =
    parameters('season,'year){ (season, year) =>
      get{
        println(s"$season $year")

        val database = WebServer.client.getDatabase("Anime")
        val collection = database.getCollection(s"$season $year")

        onSuccess(collection.find().collect().head()){ documentResult =>
          val objectMapper = new ObjectMapper()
          val r = objectMapper.createArrayNode()
          documentResult.foreach(singleDoc => r.add(objectMapper.readTree(singleDoc.toJson())))
          complete(r.toString)
        }
      }
    }
}
