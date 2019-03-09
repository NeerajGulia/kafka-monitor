import { Component, OnInit } from '@angular/core';
import { GetTopicsService } from '../get-topics.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-select-topic',
  templateUrl: './select-topic.component.html',
  styleUrls: ['./select-topic.component.css']
})
export class SelectTopicComponent implements OnInit {
  topics = [];
  selectedtopic=""
  constructor(private getTopicsService: GetTopicsService, private router:Router) { }

  ngOnInit(){
    this.getTopicsService.getTopics().subscribe((data)=>{
      this.topics = data;
      console.log(this.topics);
      
    })
  }

  getTopicDetails(){
    this.router.navigate(['/topicdetails', this.selectedtopic])
  }

}
