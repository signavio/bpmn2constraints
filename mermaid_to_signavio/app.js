import { readFile } from 'node:fs/promises';
import { rehype } from 'rehype';
import rehypeMermaid from 'rehype-mermaidjs';
import * as cheerio from 'cheerio';

class CoordinateExtractor {
    constructor() {
        this.coordinatesArray = [];
    }

    async processHtmlFile(filePath) {
        const { value } = await rehype()
        .use(rehypeMermaid, {
                     // The default strategy is 'inline-svg'
                    // strategy: 'img-png'
                     // strategy: 'img-svg'
                    // strategy: 'inline-svg'
                     // strategy: 'pre-mermaid'
                 })
            .process(await readFile(filePath, 'utf-8'));

        const $ = cheerio.load(value);
        const circleElements = $('circle');
        const rectangleElements = $('rect');

        this.extractCircleCoordinates($, circleElements);
        this.extractRectangleCoordinates($, rectangleElements);

        const jsonCoorditanes = JSON.stringify(this.coordinatesArray);
        console.log('Coordinates json: ', jsonCoorditanes);
        console.log('Coordinates Array:', this.coordinatesArray);
    }

    extractCircleCoordinates($, elements) {
        elements.each((index, element) => {
            // coordinates of the circle from initial html 
            let rx = Number($(element).attr('rx'));
            let ry = Number($(element).attr('ry'));
            let rad = Number($(element).attr('r'));

            // The transform attribute defines a list of transform definitions that are applied to an element and the element's children. 
            // Here we extract transform coordinates to bring all coordintaes to the common scale
            // find parent of the circle and ajust coordinates if some transormatio is involved 
            const translateRegex = /translate\(([\d.-]+), ([\d.-]+)\)/;
            let parentTransform = $(element).parent().attr('transform');

            // if there is transform attribute present and if it is matches to translateRegex
            if (parentTransform && translateRegex.test(parentTransform)) {
                // estract transform coordinates from transform attribute as it is a dring we use regex
                let match = parentTransform.match(translateRegex);
                let tx = Number(match[1]);
                let ty = Number(match[2]);
                // ajust circle coordinates relatively parents coordinates 
                let adjustedRx = rx + tx;
                let adjustedRy = ry + ty;
                let center = { x: adjustedRx, y: adjustedRy };
                let radius = { r: rad };

                this.coordinatesArray.push({ center, radius });
            }
        });
    }
// check if it is possible that there is no transform for parent?????? 

    extractRectangleCoordinates($, elements) {
        elements.each((index, element) => {
            // coordinates for the left top corner of the rectangle
            const x = Number($(element).attr('x'));
            const y = Number($(element).attr('y'));
            const width = Number($(element).attr('width'));
            const height = Number($(element).attr('height'));
            if (!isNaN(width) && !isNaN(height)) {
            // same logic as for circle 
            const translateRegex = /translate\(([\d.-]+), ([\d.-]+)\)/;
            const parentTransform = $(element).parent().attr('transform');

            if (parentTransform && translateRegex.test(parentTransform)) {
                const match = parentTransform.match(translateRegex);
                const tx = Number(match[1]);
                const ty = Number(match[2]);
                const adjustedRx = x + tx;
                const adjustedRy = y + ty;
                // get coordinates of all for point of the rectangle
                const topLeft = { x: adjustedRx, y: adjustedRy };
                const topRight = { x: adjustedRx + width, y: adjustedRy };
                const bottomLeft = { x: adjustedRx, y: adjustedRy - height };
                const bottomRight = { x: adjustedRx + width, y: y - height };

                
                    this.coordinatesArray.push({
                        topLeft,
                        topRight,
                        bottomLeft,
                        bottomRight,
                    });
                
            }}
        });
    }
}

const coordinateExtractor = new CoordinateExtractor();
coordinateExtractor.processHtmlFile('index.html');


