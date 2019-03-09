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
  constructor(private http: HttpClient) { }

  getTopicDetails(topic:string) {
    this.http.get('assets/topic_responce.json').subscribe((data:Topic)=>{
      this.topicDetailsSubject.next(data)
    })
     this.subscription = interval(1000).subscribe(()=>
      this.http.get('assets/topic_responce.json').subscribe((data:Topic)=>{
        this.topicDetailsSubject.next(data)
      })
    )
    this.subscriptionSubject.next(this.subscription)
  }
  modifyIntervalSubscription(value){
    this.subscription.unsubscribe()
    this.subscription = interval(value*1000).subscribe(()=>
      this.http.get('assets/topic_responce.json').subscribe((data:Topic)=>{
        this.topicDetailsSubject.next(data)
      })
    )
    this.subscriptionSubject.next(this.subscription)
  }
}
