import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { JudgeEditorComponent } from './judge-editor/judge-editor.component';
import { ScheduleContainerComponent } from './schedule-container/schedule-container.component';
import { PrintHandlerComponent } from './print-handler/print-handler.component';
import { SettingsComponent } from './settings/settings.component';

const routes: Routes = [
  {path: 'judges', component: JudgeEditorComponent},
  {path: '', component: ScheduleContainerComponent},
  {path: 'print', component: PrintHandlerComponent},
  {path: 'settings', component: SettingsComponent}
];

@NgModule({
  exports: [ RouterModule ],
  imports: [ RouterModule.forRoot(routes)]
})
export class AppRoutingModule { }
