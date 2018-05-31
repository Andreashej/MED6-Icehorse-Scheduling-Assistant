import { Component, OnInit, Input, Output, OnChanges, OnDestroy, DoCheck } from '@angular/core';
import { NgDragDropModule } from 'ng-drag-drop';
import { SettingsProviderService } from '../settings-provider.service';
import { CompetitionImporterService } from '../competition-importer.service';
import { EventEmitter } from 'events';
import { GlobalUpdateService } from '../global-update.service';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-day',
  templateUrl: './day.component.html',
  styleUrls: ['./day.component.css']
})
export class DayComponent implements OnInit, OnDestroy {
  @Input() date;
  @Input() printTemplate;
  scheduledTests = [];
  settings = {
    'days': [],
    'hours': 0,
    'name': ''
  };
  hours = [];
  blocks = [];
  saved;
  updates = false;
  subscription: Subscription;
  trackChangeSubscription: Subscription;

  onDropTest(test: any, elt) {
    const blockSize = Math.ceil((test.dragData.prel_time - 0.9) / 5);
    this.saveTest(
      test.dragData.testcode,
      test.dragData.phase,
      test.dragData.section,
      new Date(this.date),
      this.blocks.indexOf(elt),
      elt.blocktime.getTime(),
      new Date(elt.blocktime.getTime() + test.dragData.prel_time * 60000).getTime());

    elt.rowspan = blockSize;
    elt.testcode = test.dragData.testcode;
    elt.content = test.dragData;
    elt.content.state = new Date(this.date);
    elt.droppable = false;
  }

  initSchedule(tests) {
    if (tests.length > 0) {
      for (const test of tests) {
        const block = this.blocks[test.start_block];
        block.rowspan = Math.ceil((test.prel_time - 0.9) / 5);
        block.testcode = test.testcode;
        block.content = test;
        block.droppable = false;
      }
    }
  }

  constructor(private settingsProvider: SettingsProviderService,
    private competitionImporter: CompetitionImporterService,
    private updateService: GlobalUpdateService) { }

  ngOnInit() {
    this.date = new Date(this.date);
    this.getSettings();
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
    this.trackChangeSubscription.unsubscribe();
  }

  removeUnassigned(e: any, test) {
    this.scheduledTests.splice(this.scheduledTests.indexOf(test), 1);
  }

  initDays(): void {
    let blocktime = this.date;
    for (let i = 0; i <= this.settings.hours * 12; i++) {
      const block = {
        'blocktime': blocktime,
        'rowspan': 1,
        'testcode': '',
        'content': undefined,
        'droppable': true
      };
      this.blocks.push(block);
      blocktime = new Date(blocktime.getTime() + 5 * 60000);
    }
    this.getTestData();
  }

  getTestData(): void {
    this.scheduledTests = [];
    const trackstate = this.competitionImporter.activeTrack;
    this.competitionImporter.getTestData(this.date.getTime()).subscribe(
      data => this.scheduledTests = data,
      () => console.log('Error when fetching data'),
      () => {
        this.initSchedule(this.scheduledTests);
      }
    );
  }

  getSettings(): void {
    this.settingsProvider.getSettings().subscribe(
      data => this.settings = data[0],
      error => console.log('Error when fetching data'),
      () => {
        this.subscription = this.updateService.dayUpdate.subscribe(
          next => {
            console.log(next);
            console.log(this.date.getDate());
            if (next === this.date.getDate() + '&' + this.date.getMonth() + '&' + this.date.getYear() || next === '') {
              this.blocks = [];
              this.initDays();
            }
          });
          this.trackChangeSubscription = this.competitionImporter.trackChange.subscribe(
            () => {
              this.blocks = [];
              this.initDays();
            }
          );
      }
    );
}

saveTest(test, phase, section_id, state, startBlock, start, end): void {
  this.competitionImporter.saveTestState(
    test, phase, section_id, state.getTime(), startBlock, start, end).subscribe(
      () => console.log('Saving...'),
      error => console.log('Error when fetching data ' + error),
      () => console.log('Successfully saved test state')
    );
}

allowDrop(block): void {
  block.droppable = true;
  block.rowspan = 1;
}

remove(block) {
  block.testcode = '';
  block.content = undefined;
  block.droppable = true;
}
}
