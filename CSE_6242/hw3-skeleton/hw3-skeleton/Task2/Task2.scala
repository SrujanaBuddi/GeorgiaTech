package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
 
object Task2 {
  def main(args: Array[String]) {
    val sc = new SparkContext(new SparkConf().setAppName("Task2"))

    // read the file
    val file = sc.textFile("hdfs://localhost:8020" + args(0))

    // get each edge detail
    val edges = file.map(line=>line.split("\t"))

    //filter if weight is 1
    val filter_edges= edges.filter{case Array(s,e,w)=> (s.toInt,e.toInt,w.toInt)}.filter(line=>line._3!=1)

    // form value pairs of nodes and their weights
    val val_pairs_in = filter_edges.map(value=>(value._2,value._3))
    val val_pairs_out= filter_edges.map(value=>(value._1,-1*value._3))

    // sum the weight
    val weight_sum = (val_pairs_in ++ val_pairs_out).reduceByKey(_ + _)
 
    //save the result to a file
    val output = weight_sum.map(x=>Array(x._1.toString,x._2.toString)).map(value=>value.mkString("\t"))

    output.saveAsTextFile("hdfs://localhost:8020" + args(1))
  }
}
