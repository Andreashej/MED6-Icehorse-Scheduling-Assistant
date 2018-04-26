import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CompetitionImporterService } from '../competition-importer.service';

@Component({
  selector: 'app-test-card-schedule',
  templateUrl: './test-card-schedule.component.html',
  styleUrls: ['./test-card-schedule.component.css']
})
export class TestCardScheduleComponent implements OnInit {
  @Input() test;
  @Output() testGrab = new EventEmitter();
  @Output() testGrabStart = new EventEmitter();

  hours = 0;
  minutes = 0;
  free_left = 0;
  free_right = 0;
  split_rr = 0;
  split_lr = 0;
  join_section = 0;

  constructor(private competitionImporter: CompetitionImporterService) { }

  ngOnInit() {
    this.hours = Math.floor(this.test.prel_time / 60);
    this.minutes = this.test.prel_time % 60;
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

  split() {
    this.competitionImporter.split(this.test.testcode, this.test.phase, this.test.section, this.split_lr, this.split_rr).subscribe(
      () => console.log('Split test ' + this.test.testcode)
    );
  }

  join() {
    this.competitionImporter.join(this.test.testcode, this.test.phase, this.join_section, this.test.section).subscribe(
      () => console.log('Joined test' + this.test.testcode)
    );
  }

}
