import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { NgDragDropModule } from 'ng-drag-drop';
import { FormsModule } from '@angular/forms';


import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { UnassignedTestsComponent } from './unassigned-tests/unassigned-tests.component';

import { CompetitionImporterService } from './competition-importer.service';
import { SettingsProviderService } from './settings-provider.service';

import { TestCardComponent } from './test-card/test-card.component';
import { ScheduleComponent } from './schedule/schedule.component';
import { DayComponent } from './day/day.component';

import { TestCardScheduleComponent } from './test-card-schedule/test-card-schedule.component';


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    UnassignedTestsComponent,
    TestCardComponent,
    ScheduleComponent,
    DayComponent,
    TestCardScheduleComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    NgDragDropModule.forRoot(),
    BrowserModule,
    FormsModule
  ],
  providers: [
    CompetitionImporterService,
    SettingsProviderService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
