import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { NgDragDropModule } from 'ng-drag-drop';


import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { UnassignedTestsComponent } from './unassigned-tests/unassigned-tests.component';

import { CompetitionImporterService } from './competition-importer.service';
import { SettingsProviderService } from './settings-provider.service';

import { TestCardComponent } from './test-card/test-card.component';
import { ScheduleComponent } from './schedule/schedule.component';
import { DayComponent } from './day/day.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    UnassignedTestsComponent,
    TestCardComponent,
    ScheduleComponent,
    DayComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    NgDragDropModule.forRoot(),
    BrowserModule,
    BrowserAnimationsModule
  ],
  providers: [
    CompetitionImporterService,
    SettingsProviderService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
