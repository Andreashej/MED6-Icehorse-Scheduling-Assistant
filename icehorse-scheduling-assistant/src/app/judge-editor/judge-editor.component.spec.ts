import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JudgeEditorComponent } from './judge-editor.component';

describe('JudgeEditorComponent', () => {
  let component: JudgeEditorComponent;
  let fixture: ComponentFixture<JudgeEditorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JudgeEditorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JudgeEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
