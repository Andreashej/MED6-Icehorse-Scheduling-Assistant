import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TestCardScheduleComponent } from './test-card-schedule.component';

describe('TestCardScheduleComponent', () => {
  let component: TestCardScheduleComponent;
  let fixture: ComponentFixture<TestCardScheduleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestCardScheduleComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestCardScheduleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
