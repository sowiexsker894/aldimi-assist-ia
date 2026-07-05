import { ChangeDetectionStrategy, Component } from '@angular/core';
import { DniOcrFlowComponent } from './dni-ocr-flow.component';

@Component({
  selector: 'app-dni-page',
  imports: [DniOcrFlowComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './dni-page.component.html',
})
export class DniPageComponent {}
