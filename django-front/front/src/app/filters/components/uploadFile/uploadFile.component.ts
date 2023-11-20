import { Component, EventEmitter, Input, Output } from '@angular/core';
import {
  FileRemoveEvent,
  FileSelectEvent,
  Filter,
  ImagesSrcOut,
  IndexedImages,
  UploadEvent,
} from '../../interfaces';
import { FiltersService } from '../../services/filters.service';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-upload-file',
  templateUrl: './uploadFile.component.html',
  styles: [],
})
export class UploadFileComponent {
  @Input({ required: true }) canUpload!: boolean;
  @Input({ required: true }) kernel!: number;
  @Input({ required: true }) sigma!: number;
  @Input({ required: true }) selectedFilter!: Filter | undefined;

  @Output()
  public onImageSrcOut: EventEmitter<ImagesSrcOut> = new EventEmitter();

  @Output()
  public onImageConvIn: EventEmitter<IndexedImages> = new EventEmitter();

  @Output()
  public onIsLoading: EventEmitter<boolean> = new EventEmitter();

  public imageSrcIn!: IndexedImages;
  public imageSrcOut!: ImagesSrcOut;
  public imageConvIn!: IndexedImages;
  public disabled: boolean = false;
  public isLoading: boolean = false;

  public uploadedFiles: any[] = [];

  constructor(
    private filtersService: FiltersService,
    private messageService: MessageService
  ) {}

  onUpload(event: UploadEvent) {
    const file = event.files[0];
    this.imageConvIn = {
      index: file.name,
      image: URL.createObjectURL(file),
    };

    this.convolution(file);

    this.imageSrcIn = {
      index: '',
      image: '',
    };
  }

  indexImages(event: FileSelectEvent) {
    const file = event.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        const indexedImage: IndexedImages = {
          index: file.name,
          image: e.target.result,
        };
        this.imageSrcIn = indexedImage;
      };
      reader.readAsDataURL(file);
    }
  }

  removeImage(event: FileRemoveEvent) {
    this.imageSrcIn = {
      index: '',
      image: '',
    };
  }

  onProgress(event: any) {
    this.disabled = true;
    this.canUpload = false;
    this.isLoading = true;
    this.emitIsLoading();
  }

  convolution(file: File) {
    this.filtersService
      .makeConvolution({
        image: file,
        kernel_size: this.kernel,
        sigma: this.sigma,
        filter_name: this.selectedFilter!.name.toLowerCase(),
      })
      .subscribe({
        next: (response) => {
          this.imageSrcOut = {
            index: file.name,
            image: `data:image/jpeg;base64,${response.image}`,
            time: `${response.time_taken}`,
            thread_per_block: `${response.threads_per_block}`,
            number_of_blocks: `${response.number_of_blocks}`,
            method: `${response.method}`,
            kernel: `${response.kernel}`,
            sigma: `${response.sigma}`,
          };
        },
        complete: () => {
          this.messageService.add({
            severity: 'success',
            summary: 'Imagen Procesada',
            detail: '',
          });
          this.blockValues();
        },
        error: (e) => console.log(e),
      });
  }

  blockValues() {
    this.emitImagesSrcOut();
    this.emitImagesConvIn();
    this.isLoading = false;
    this.emitIsLoading();
    this.disabled = false;
    this.canUpload = true;
  }

  emitImagesSrcOut(): void {
    this.onImageSrcOut.emit({ ...this.imageSrcOut! });
    this.imageSrcOut = {
      index: '',
      image: '',
      time: '',
      thread_per_block: '',
      number_of_blocks: '',
      method: '',
      kernel: '',
      sigma: '',
    };
  }

  emitImagesConvIn(): void {
    this.onImageConvIn.emit({ ...this.imageConvIn! });
    this.imageConvIn = {
      index: '',
      image: '',
    };
  }

  emitIsLoading(): void {
    this.onIsLoading.emit(this.isLoading);
  }
}
