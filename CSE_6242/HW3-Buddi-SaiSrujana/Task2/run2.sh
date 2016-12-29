spark-submit --class edu.gatech.cse6242.Task2 --master local \
  target/task2-1.0.jar /user/cse6242/graph2.tsv /user/cse6242/task2output2

hadoop fs -getmerge /user/cse6242/task2output2 task2output2.tsv
hadoop fs -rm -r /user/cse6242/task2output2
