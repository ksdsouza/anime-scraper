package io.github.ksdsouza.WebServer

import akka.http.scaladsl.model._
import akka.http.scaladsl.server.Directives._

object GetRouter {
  val route =
    parameters('season,'year){ (season, year) =>
      get{
        complete(HttpEntity(ContentTypes.`text/html(UTF-8)`, "Hello World"))
      }
    }
}
