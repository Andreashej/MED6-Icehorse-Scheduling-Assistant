import { Component, OnInit, Input, Output } from '@angular/core';
import { NgDragDropModule } from 'ng-drag-drop';
import { SettingsProviderService } from '../settings-provider.service';
import { CompetitionImporterService } from '../competition-importer.service';
import { EventEmitter } from 'events';

@Component({
  selector: 'app-day',
  templateUrl: './day.component.html',
  styleUrls: ['./day.component.css']
})
export class DayComponent implements OnInit {
  @Input() date;
  scheduledTests = [];
  settings = {
    'days': [],
    'hours': 0,
    'name': ''
  };
  hours = [];
  blocks = [];
  saved;

  onDropTest(test: any, elt) {
    const blockSize = Math.ceil(test.dragData.prel_time / 5);
    this.saveTest(test.dragData.testcode, test.dragData.phase, test.dragData.section, this.date, this.blocks.indexOf(elt));
    elt.rowspan = blockSize;
    elt.testcode = test.dragData.testcode;
    elt.content = test.dragData;
    elt.droppable = false;
    // this.scheduledTests.push(test.dragData);
  }

  initSchedule(tests) {
    if (tests.length > 0) {
      for (const test of tests) {
        const block = this.blocks[test.start_block];
        block.rowspan = Math.ceil(test.prel_time / 5);
        block.testcode = test.testcode;
        block.content = test;
        block.droppable = false;
      }
    }
  }

  constructor(private settingsProvider: SettingsProviderService, private competitionImporter: CompetitionImporterService) { }

  ngOnInit() {
    this.getSettings();
  }

  removeUnassigned(e: any, test) {
    this.scheduledTests.splice(this.scheduledTests.indexOf(test), 1);
  }

  initDays(): void {
    let blocktime = new Date(this.date);

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
    this.getTestData(this.date);
  }

  getTestData(date): void {
    this.competitionImporter.getTestData(date).subscribe(
      data => this.scheduledTests = data,
      () => console.log('Error when fetching data'),
      () => this.initSchedule(this.scheduledTests)
    );
  }

  getSettings(): void {
    this.settingsProvider.getSettings().subscribe(
      data => this.settings = data[0],
      error => console.log('Error when fetching data'),
      () => this.initDays()
    );
  }

  saveTest(test, phase, section_id, state, startBlock): void {
    this.competitionImporter.saveTestState(test, phase, section_id, state, startBlock).subscribe(
      data => this.saved = data,
      error => console.log('Error when fetching data'),
      () => console.log('Successfully saved test state')
    );
  }

  allowDrop(block): void {
    block.rowspan = 1;
    block.droppable = true;
  }

  remove(block) {
    block.testcode = '';
    block.content = undefined;
    block.droppable = true;
  }
}
