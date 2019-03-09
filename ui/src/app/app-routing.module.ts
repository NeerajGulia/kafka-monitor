import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SelectTopicComponent } from './select-topic/select-topic.component';
import { TopicDetailsComponent } from './topic-details/topic-details.component';

const routes: Routes = [
  {path:'', component:SelectTopicComponent},
  {path:'topicdetails/:topicid', component:TopicDetailsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
