name := "puzzles"

version := "0.1"

scalaVersion := "2.12.7"

libraryDependencies += "org.scalactic" %% "scalactic" % "3.0.5"
libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.5" % "test"

addCompilerPlugin("io.tryp" % "splain" % "0.3.4" cross CrossVersion.patch)

scalacOptions += "-P:splain:implicits:true"

// mainClass in (Compile, run) := Some("chandrima_xor")