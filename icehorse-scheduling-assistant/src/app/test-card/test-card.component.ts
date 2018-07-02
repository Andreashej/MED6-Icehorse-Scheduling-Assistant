import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { NgDragDropModule } from 'ng-drag-drop';
import { CompetitionImporterService } from '../competition-importer.service';
import { GlobalUpdateService } from '../global-update.service';

@Component({
  selector: 'app-test-card',
  templateUrl: './test-card.component.html',
  styleUrls: ['./test-card.component.css']
})
export class TestCardComponent implements OnInit {
  @Input() test;
  @Output() _toggleFinal = new EventEmitter();
  hours = 0;
  minutes = 0;
  free_left = 0;
  free_right = 0;

  @Output() testGrab = new EventEmitter();

  constructor(private competitionImporter: CompetitionImporterService, private updateService: GlobalUpdateService) {
  }

  testGrabbed(e: any) {
    this.testGrab.emit(e);
  }

  ngOnInit() {
    this.hours = Math.floor(this.test.prel_time / 60);
    this.minutes = Math.round((this.test.prel_time % 60) * 10) / 10;
    if (this.test.riders_per_heat > 1) {
      this.free_left = this.test.left_heats * 3 - this.test.left_rein;
      this.free_right = this.test.right_heats * 3 - this.test.right_rein;
    }
  }

  toggleFinal(phase: string) {
    this.competitionImporter.toggleFinal(this.test._id, phase).subscribe(
      update => this.test = update,
      () => console.log('Error on final toggle'),
      () => {
        this.updateService.updateUnassigned();
      }
    );
  }

}
