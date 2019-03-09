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
  scale = [{ name: '30 Sec', value: 30}, { name: '1 Min', value: 60}, { name: '2 Min', value: 120}, { name: '5 Min', value: 300}];
  val = 30
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
          label: 'Consumer Lag',
          backgroundColor: '#42A5F5',
          borderColor: '#1E88E5',
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
        labels.push(element.cname)
        data_value.push(element.lag)
      });
      this.consumers['labels'] = labels
      this.consumers['datasets'][0]['data'] = data_value
      this.consumers = Object.assign({}, this.consumers)
      this.updateArrivalGraph(this.val)

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
    for (let i = value; i > 0; i--) {
      labels.push(i)
      data_value.push(0)
    }
    this.topic.arrivalrate.forEach((element, index) => {
      data_value[data_value.length - this.topic.arrivalrate.length + index] = Math.random()
    });
    this.arrival_rate['labels'] = labels
    this.arrival_rate['datasets'][0]['data'] = data_value
    this.arrival_rate = Object.assign({}, this.arrival_rate)
    this.topic_arrival_rate = this.topic.arrivalrate[this.topic.arrivalrate.length - 1]
  }

}
