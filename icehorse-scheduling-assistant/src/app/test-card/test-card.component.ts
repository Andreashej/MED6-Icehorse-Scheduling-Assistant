import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { NgDragDropModule } from 'ng-drag-drop';

@Component({
  selector: 'app-test-card',
  templateUrl: './test-card.component.html',
  styleUrls: ['./test-card.component.css']
})
export class TestCardComponent implements OnInit {
  @Input() test;

  @Output() testGrab = new EventEmitter();

  constructor() { }

  testGrabbed(e: any) {
    this.testGrab.emit(e);
  }

  ngOnInit() {
  }

}
