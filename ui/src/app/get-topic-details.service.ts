import { Injectable } from '@angular/core';
import { Observable, interval, BehaviorSubject, Subscription } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Topic } from './topic';


@Injectable({
  providedIn: 'root'
})
export class GetTopicDetailsService {

  topicDetailsSubject: BehaviorSubject<Topic> = new BehaviorSubject<Topic>(new Topic())
  subscriptionSubject: BehaviorSubject<Subscription> = new BehaviorSubject<Subscription>(new Subscription())
  subscription: Subscription
  url: string = "http://localhost:9999/api/arrivalrate/"
  completeurl = "";
  constructor(private http: HttpClient) { }

  getTopicDetails(topic:string) {
    this.completeurl=this.url+topic;
    this.http.get(this.completeurl).subscribe((data:Topic)=>{
      this.topicDetailsSubject.next(data)
    })
     this.subscription = interval(1000).subscribe(()=>
      this.http.get(this.completeurl).subscribe((data:Topic)=>{
        this.topicDetailsSubject.next(data)
      })
    )
    this.subscriptionSubject.next(this.subscription)
  }
  modifyIntervalSubscription(value){
    this.subscription.unsubscribe()
    this.subscription = interval(value*1000).subscribe(()=>
      this.http.get(this.completeurl).subscribe((data:Topic)=>{
        this.topicDetailsSubject.next(data)
      })
    )
    this.subscriptionSubject.next(this.subscription)
  }
}
