import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { GetTopicDetailsService } from '../get-topic-details.service';
import { Topic } from '../topic';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-topic-details',
  templateUrl: './topic-details.component.html',
  styleUrls: ['./topic-details.component.css']
})
export class TopicDetailsComponent implements OnInit {
  consumers = {}
  arrival_rate = {}
  memory_consumption={}
  scale = [{ name: '5Min', value: 300}, { name: '10Min', value: 600}, { name: '15Min', value: 900}];
  val = 300
  topic_arrival_rate = 0
  topic: Topic = new Topic()
  subsription: Subscription;
  options = {}
  constructor(private route: ActivatedRoute, private getTopicDetailsService: GetTopicDetailsService,
    private changeDetector: ChangeDetectorRef) {
    this.consumers = {
      labels: [],
      datasets: [
        {
          label: 'Partition 0',
          backgroundColor: '#42A5F5',
          borderColor: '#1E88E5',
          data: []
        },
        {
          label: 'Partition 1',
          backgroundColor: '#423452',
          borderColor: '#423452',
          data: []
        }

      ]
    }
    this.options = {
      animation: false,
    }

    this.arrival_rate = {
      labels: [],
      datasets: [
        {
          label: 'Arrival Rate',
          borderColor: '#42A5F5',
          fill: false,
          data: []
        }
      ]

    }

    this.memory_consumption = {
      labels: [],
      datasets: [
        {
          label: 'Free physical memory size',
          borderColor: '#42A5F5',
          fill: false,
          data: []
        },
        {
          label: 'Commited virtual memory size',
          borderColor: '#423452',
          fill: false,
          data: []
        },
        {
          label: 'Free swap space size',
          borderColor: '#97822F',
          fill: false,
          data: []
        }
      ]

    }

  }

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('topicid');
    this.getTopicDetailsService.getTopicDetails(id)
    this.getTopicDetailsService.subscriptionSubject.subscribe((data) => {
      this.subsription = data
    })
    this.getTopicDetailsService.topicDetailsSubject.subscribe((data: Topic) => {
      this.topic = data;
      
      let labels = []
      let data_value = []
      // let physical_mem=[]
      // let virtual_mem=[]
      // let swap_mem=[]

      // this.topic.memory_consumption.forEach(element => {
      //   labels.push(element.cname)
      //   data_value.push(element.lag)
      // });

      this.topic.consumers.forEach(element => {
        labels.push(element.name)
        
        element.partitions.forEach((data, index)=>{
          if (!data_value[index]){
            data_value[index]=[]
          }
          data_value[index].push(data.Lag)
        })
        // data_value.push(element.partitions[0].Lag)
      });
      this.consumers['labels'] = labels
      data_value.forEach((data, index)=>{
        this.consumers['datasets'][index]['data'] = data
      })
      
      this.consumers = Object.assign({}, this.consumers)
      this.updateArrivalGraph(this.val)
      console.log(this.consumers)


    })

  }
  ngOnDestroy() {
    this.subsription.unsubscribe()
  }
  handleGraphScaleChange(value) {
    if (value != this.arrival_rate['labels'].length) {
      this.val = value
      
      this.updateArrivalGraph(value)
    }
  }

  updateArrivalGraph(value) {
    let labels = []
    let data_value = []
    for (let i = value; i > 0; i-=10) {
      labels.push(i)
      data_value.push(0)
    }
    this.topic.ArrivalRate.forEach((element, index) => {
      data_value[data_value.length - this.topic.ArrivalRate.length + index] = element
    });
    this.arrival_rate['labels'] = labels
    this.arrival_rate['datasets'][0]['data'] = data_value
    this.arrival_rate = Object.assign({}, this.arrival_rate)
    this.topic_arrival_rate = this.topic.ArrivalRate[this.topic.ArrivalRate.length - 1]
  }

}
