hadoop jar ./target/task1-1.0.jar edu.gatech.cse6242.Task1 /user/cse6242/graph2.tsv /user/cse6242/task1output2
hadoop fs -getmerge /user/cse6242/task1output2/ task1output2.tsv
hadoop fs -rm -r /user/cse6242/task1output2
