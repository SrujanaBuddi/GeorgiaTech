package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object Task2 {
  def main(args: Array[String]) {
    val sc = new SparkContext(new SparkConf().setAppName("Task2"))

    // read the file
    val file = sc.textFile("hdfs://localhost:8020" + args(0))

    /* TODO: Needs to be implemented */

    // store output on given HDFS path.
    // YOU NEED TO CHANGE THIS
    file.saveAsTextFile("hdfs://localhost:8020" + args(1))
  }
}
