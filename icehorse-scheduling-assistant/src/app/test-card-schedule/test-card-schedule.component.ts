import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CompetitionImporterService } from '../competition-importer.service';
import { GlobalUpdateService } from '../global-update.service';

@Component({
  selector: 'app-test-card-schedule',
  templateUrl: './test-card-schedule.component.html',
  styleUrls: ['./test-card-schedule.component.css']
})
export class TestCardScheduleComponent implements OnInit {
  @Input() test;
  @Input() rowspan;
  @Input() starttime;
  @Output() testGrab = new EventEmitter();
  @Output() testGrabStart = new EventEmitter();

  hours = 0;
  minutes = 0;
  free_left = 0;
  free_right = 0;
  split_rr = 0;
  split_lr = 0;
  join_section = 0;
  judgeList = [];
  endtime;

  constructor(private competitionImporter: CompetitionImporterService, private updateService: GlobalUpdateService) { }

  ngOnInit() {
    this.test.state = new Date(this.test.state);
    this.hours = Math.floor(this.test.prel_time / 60);
    this.minutes = this.test.prel_time % 60;
    this.endtime = new Date(this.starttime.getTime() + this.test.prel_time * 60000);
    if (this.test.riders_per_heat > 1) {
      this.free_left = this.test.left_heats * 3 - this.test.left_rein;
      this.free_right = this.test.right_heats * 3 - this.test.right_rein;
    }
    this.getJudges();

    this.updateService.update.subscribe(
      next => this.onUpdate(next),
      () => console.log('Error on update')
    );
  }

  onUpdate(next): void {
    console.log(next);
    if (next === 'judges&' + this.test.testcode ) {
      this.getJudges();
    }
    this.hours = Math.floor(this.test.prel_time / 60);
    this.minutes = this.test.prel_time % 60;
    this.endtime = new Date(this.starttime.getTime() + this.test.prel_time * 60000);
    if (this.test.riders_per_heat > 1) {
      this.free_left = this.test.left_heats * 3 - this.test.left_rein;
      this.free_right = this.test.right_heats * 3 - this.test.right_rein;
    }
  }

  testGrabbed(e: any) {
    this.testGrab.emit(e);
  }

  grabStart(e: any) {
    this.testGrabStart.emit(e);
  }

  splitTest(): void {
    this.competitionImporter.split(this.test.testcode, this.test.phase, this.test.section, this.split_lr, this.split_rr).subscribe(
      () => console.log('Next'),
      () => console.log('Error with split'),
      () => this.updateService.doUpdate(this.test.testcode)
    );
  }

  joinTest(): void {
    this.competitionImporter.join(this.test.testcode, this.test.phase, this.join_section - 1, this.test.section).subscribe(
      () => console.log('Next'),
      () => console.log('Error with join'),
      () => this.updateService.doUpdate(this.test.testcode)
    );
  }

  addJudge(fname: string, lname: string) {
    this.competitionImporter.addJudge(this.test.testcode,
                                      this.test.phase,
                                      fname,
                                      lname,
                                      this.test.state.getTime()).subscribe(
      () => this.updateService.doUpdate('judges&' + this.test.testcode),
      () => console.log('Error when adding judge')
    );
  }

  removeJudge(fname: string, lname: string) {
    this.competitionImporter.removeJudge(this.test.testcode,
                                        this.test.phase,
                                        fname,
                                        lname,
                                        this.test.state.getTime()).subscribe(
      () => this.updateService.doUpdate('judges&' + this.test.testcode),
      () => console.log('Error when removing judge')
    );
  }

  getJudges() {
    this.competitionImporter.getJudgesForTest(this.test.testcode, this.test.phase, this.test.state.getTime()).subscribe(
      judges => this.judgeList = judges
    );
  }

  toDate(date: string): Date {
    return new Date(date);
  }

  toggleFinal(phase: string) {
    this.competitionImporter.toggleFinal(this.test.testcode, phase).subscribe(
      update => this.test = update,
      () => console.log('Error when toggling final'),
      () => this.updateService.doUpdate('finaltoggle&' + this.test.testcode + '&' + phase)
    );
  }
}
