import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { GetTopicsService } from './get-topics.service';
import { GetTopicDetailsService } from './get-topic-details.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Panda';
  val=1;

  constructor( private router: Router, private getTopicDetailsService: GetTopicDetailsService){
    
  }

  handleIntervalChange(event){
    this.getTopicDetailsService.modifyIntervalSubscription(event.value)
  }

  
}
