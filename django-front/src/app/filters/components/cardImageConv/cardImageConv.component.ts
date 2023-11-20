import { Component, Input } from '@angular/core';
import { ImagesSrcOut } from '../../interfaces';

@Component({
  selector: 'app-card-image-conv',
  templateUrl: './cardImageConv.component.html',
  styles: [``],
})
export class CardImageConvComponent {

  @Input({required: true}) image!: ImagesSrcOut;

}
