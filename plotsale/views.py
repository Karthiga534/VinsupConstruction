from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([AllowAny])
def get_property_types(request):
    property_types = PropertyType.objects.all()
    serializer = PropertyTypeSerializer(property_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_plot_types(request):
    plot_types = PlotType.objects.all()
    serializer = PlotTypeSerializer(plot_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_soil_types(request):
    soil_types = SoilType.objects.all()
    serializer = SoilTypeSerializer(soil_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_status_types(request):
    status = Status.objects.all()
    serializer = StatusSerializer(status, many=True)
    return Response(serializer.data)

#------------------------------------------------ Site Posting -----------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def site_postings(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                posting = SitePosting.objects.get(pk=pk)
                serializer = SitePostingSerializer(posting)
                return Response(serializer.data)
            except SitePosting.DoesNotExist:
                return Response({'error': 'SitePosting not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            postings = SitePosting.objects.all()
            serializer = SitePostingSerializer(postings, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SitePostingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def site_posting_detail(request, pk):
    try:
        posting = SitePosting.objects.get(pk=pk)
    except SitePosting.DoesNotExist:
        return Response({'error': 'SitePosting not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SitePostingSerializer(posting)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SitePostingSerializer(posting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        posting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#------------------------------------------------ Queries -----------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def queries(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                posting = Queries.objects.get(pk=pk)
                serializer = QueriesSerializer(posting)
                return Response({
                    'message': 'Query details retrieved successfully',
                    'data': serializer.data
                })
            except Queries.DoesNotExist:
                return Response({
                    'error': 'Query not found'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            postings = Queries.objects.all()
            serializer = QueriesSerializer(postings, many=True)
            return Response({
                'message': 'All queries retrieved successfully',
                'data': serializer.data
            })
    
    elif request.method == 'POST':
        serializer = QueriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Query created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': 'Failed to create query',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def queries_detail(request, pk):
    try:
        posting = Queries.objects.get(pk=pk)
    except Queries.DoesNotExist:
        return Response({'error': 'Queries not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QueriesSerializer(posting)
        return Response({'message': 'Your details', 'data': serializer.data})

    elif request.method == 'PUT':
        serializer = QueriesSerializer(posting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Updated successfully', 'data': serializer.data})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        posting.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
#------------------------------------------------ Plot Sales -----------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def plotsales(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                plotsale = PlotSales.objects.get(pk=pk)
                serializer = PlotSalesSerializer(plotsale)
                return Response({
                    'message': 'Plot Sales details retrieved successfully',
                    'data': serializer.data
                })
            except PlotSales.DoesNotExist:
                return Response({
                    'error': 'Plot Sales not found'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            plotsales = PlotSales.objects.all()
            serializer = PlotSalesSerializer(plotsales, many=True)
            return Response({
                'message': 'All Plot Sales retrieved successfully',
                'data': serializer.data
            })
    
    elif request.method == 'POST':
        serializer = PlotSalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Plot Sales created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': 'Failed to create query',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def plotsales_detail(request, pk):
    try:
        plotsale = PlotSales.objects.get(pk=pk)
    except PlotSales.DoesNotExist:
        return Response({'error': 'Queries not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlotSalesSerializer(plotsale)
        return Response({'message': 'Your details', 'data': serializer.data})

    elif request.method == 'PUT':
        serializer = PlotSalesSerializer(plotsale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Updated successfully', 'data': serializer.data})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        plotsale.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)